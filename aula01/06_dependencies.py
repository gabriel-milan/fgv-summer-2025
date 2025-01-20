from pathlib import Path
from random import random
from uuid import uuid4

import pandas as pd
import requests
from prefect import flow, task

TMP_DIR = Path("/tmp")
PROBABILITY_OF_FAILURE = 0.5


@task(retries=3)
def get_data(csv_url: str) -> Path:
    """
    Function to get data. Downloads the CSV file from the URL into the current directory.
    """
    if random() >= PROBABILITY_OF_FAILURE:
        raise ValueError("Failed to download data")
    response = requests.get(csv_url)
    fname = TMP_DIR / f"{uuid4()}.csv" # Unique filename in temporary directory
    with open(fname, "wb") as file:
        file.write(response.content)
    return fname


@task
def transform_data(raw_data_path: Path) -> Path:
    """
    Function to transform data. Reads the CSV file from the raw data directory, perform some
    transformations and saves the result in the interim data directory.
    """
    df = pd.read_csv(raw_data_path)
    # Rename "locequip" column to "local"
    df.rename(columns={"locequip": "local"}, inplace=True)
    # Save the result in the interim data directory
    fname = TMP_DIR / f"{uuid4()}.csv"
    df.to_csv(fname, index=False)
    return fname


@task
def show_data(transformed_data_path: Path) -> None:
    """
    Group by "bairro" column and show the top 5 neighborhoods with the most cameras.
    """
    df = pd.read_csv(transformed_data_path)
    print(df["bairro"].value_counts(sort=True).head(5))


@flow(log_prints=True)
def main():
    raw_data_path = get_data(
        "https://raw.githubusercontent.com/prefeitura-rio/storage/refs/heads/master/camera_numero.csv"
    )
    transformed_data_path = transform_data(raw_data_path=raw_data_path)
    show_data(transformed_data_path)


if __name__ == "__main__":
    main()