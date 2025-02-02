from pathlib import Path
from uuid import uuid4

import pandas as pd
from prefect import flow, task

from data_generator import generate_data
from gcp import upload_to_gcs_and_create_biglake

# Convert Python functions into Prefect tasks (using the `task` decorator)
task_generate_data = task(generate_data)
task_upload_to_gcs_and_create_biglake = task(upload_to_gcs_and_create_biglake)


@task
def save_data(df: pd.DataFrame) -> Path:
    """
    Save the DataFrame to a temporary CSV file and return the path.

    Args:
        df (pd.DataFrame): DataFrame to save

    Returns:
        str: Path to the saved CSV file
    """
    path = Path(f"/tmp/{uuid4()}.csv")
    df.to_csv(path, index=False)
    return path


# Define the flow
@flow(log_prints=True)
def main():
    # Generate some data
    data = task_generate_data(n_rows=1000)

    # Save the data to a temporary CSV file
    path = save_data(df=data)

    # Upload the CSV file to GCS and create a BigLake table
    task_upload_to_gcs_and_create_biglake(
        local_file_path=path,
        project_id="emap-summer-2025",
        dataset_id="publico_jaffle_shop",
        table_name="aula02",
        region="us-central1",
        file_format="CSV",
    )


if __name__ == "__main__":
    main()
