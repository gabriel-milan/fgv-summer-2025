"""
Script to upload a local file to GCS and create a BigLake table with auto-inferred schema
"""

from google.cloud import storage
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
from typing import List


def infer_schema_from_file(
    file_path: str, file_format: str
) -> List[bigquery.SchemaField]:
    """
    Infer BigQuery schema from file
    """
    # Map pandas dtypes to BigQuery types
    type_mapping = {
        "object": "STRING",
        "int64": "INTEGER",
        "float64": "FLOAT",
        "bool": "BOOLEAN",
        "datetime64[ns]": "STRING",
        "date": "STRING",
    }

    if file_format.upper() == "CSV":
        # Read first few rows of CSV to infer schema
        df = pd.read_csv(file_path, nrows=1000)
        schema = []

        for column, dtype in df.dtypes.items():
            bq_type = type_mapping.get(str(dtype), "STRING")
            schema.append(bigquery.SchemaField(column, bq_type))

        return schema

    elif file_format.upper() == "PARQUET":
        # For Parquet, read the schema directly
        df = pd.read_parquet(file_path)
        schema = []

        for column, dtype in df.dtypes.items():
            # Convert datetime columns to string format
            if str(dtype).startswith("datetime"):
                df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")

            bq_type = type_mapping.get(str(dtype), "STRING")
            schema.append(bigquery.SchemaField(column, bq_type))

        # Save the modified dataframe back to parquet
        df.to_parquet(file_path, index=False)

        return schema

    else:
        raise ValueError(f"Unsupported file format: {file_format}")


def create_dataset_if_not_exists(
    bq_client: bigquery.Client, project_id: str, dataset_id: str
):
    """
    Create a BigQuery dataset if it doesn't exist

    Args:
        bq_client: BigQuery client instance
        project_id: Google Cloud project ID
        dataset_id: BigQuery dataset ID to create
    """
    dataset_ref = f"{project_id}.{dataset_id}"
    try:
        bq_client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_ref} already exists")
    except Exception:
        # Dataset does not exist, create it
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # Specify the location
        dataset = bq_client.create_dataset(dataset)
        print(f"Created dataset {dataset_ref}")


def upload_to_gcs_and_create_biglake(
    local_file_path: str,
    project_id: str,
    dataset_id: str,
    table_name: str,
    file_format: str = "CSV",
):
    """
    Upload a local file to GCS and create a BigLake table with auto-inferred schema

    Args:
        local_file_path: Path to local file to upload
        project_id: Google Cloud project ID
        dataset_id: BigQuery dataset ID (will be used as bucket name)
        table_name: Name of the table to create
        file_format: Format of the input file (CSV or PARQUET)
    """
    try:
        # Check if GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set"
            )

        # Initialize GCS client
        storage_client = storage.Client(project=project_id)

        # Initialize BigQuery client
        bq_client = bigquery.Client(project=project_id)

        # Create dataset if it doesn't exist
        create_dataset_if_not_exists(bq_client, project_id, dataset_id)

        # Delete table if it exists
        table_id = f"{project_id}.{dataset_id}.{table_name}"
        try:
            bq_client.delete_table(table_id)
            print(f"Table {table_id} deleted")
        except Exception:
            print(f"Table {table_id} does not exist")

        # Create or get bucket (using dataset_id as bucket name)
        bucket_name = dataset_id.lower()  # GCS bucket names must be lowercase
        try:
            bucket = storage_client.create_bucket(bucket_name)
            print(f"Bucket {bucket_name} created")
        except Exception:
            bucket = storage_client.get_bucket(bucket_name)
            print(f"Using existing bucket: {bucket_name}")

        # Upload file to GCS
        blob_name = f"{table_name}/{os.path.basename(local_file_path)}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_file_path)
        print(f"File uploaded to gs://{bucket_name}/{blob_name}")

        # Infer schema from file
        schema = infer_schema_from_file(local_file_path, file_format)
        print("Inferred schema:")
        for field in schema:
            print(f"- {field.name}: {field.field_type}")

        # Create BigLake table
        gcs_uri = f"gs://{bucket_name}/{blob_name}"

        # Create external table definition
        external_config = bigquery.ExternalConfig(file_format.upper())
        external_config.source_uris = [gcs_uri]
        external_config.schema = schema

        if file_format.upper() == "CSV":
            external_config.options.skip_leading_rows = 1  # Skip header row
            external_config.options.allow_quoted_newlines = True

        # Create table
        table_id = f"{project_id}.{dataset_id}.{table_name}"
        table = bigquery.Table(table_id)
        table.external_data_configuration = external_config

        table = bq_client.create_table(table)
        print(f"Created BigLake table: {table_id}")

    except Exception as e:
        print(f"Error: {str(e)}")


# Example usage
if __name__ == "__main__":
    params = {
        "local_file_path": "./data/sample_employees.csv",
        "project_id": "project_id",
        "dataset_id": "dataset_id",
        "table_name": "table_name",
        "file_format": "CSV",  # or "PARQUET"
    }

    upload_to_gcs_and_create_biglake(**params)
