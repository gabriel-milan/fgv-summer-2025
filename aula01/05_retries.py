from pathlib import Path
from random import random

import pandas as pd
import requests
from prefect import flow, task


RAW_DIRECTORY = Path(__file__).parent / "data" / "raw"
INTERIM_DIRECTORY = Path(__file__).parent / "data" / "interim"
PROBABILITY_OF_FAILURE = 0.5


@task(retries=3)
def get_data(csv_url: str) -> None:
    """
    Function to get data. Downloads the CSV file from the URL into the current directory.
    """
    if random() >= PROBABILITY_OF_FAILURE:
        raise ValueError("Failed to download data")
    response = requests.get(csv_url)
    RAW_DIRECTORY.mkdir(parents=True, exist_ok=True)
    with open(RAW_DIRECTORY / "data.csv", "wb") as file:
        file.write(response.content)


@task
def transform_data() -> None:
    """
    Function to transform data. Reads the CSV file from the raw data directory, perform some
    transformations and saves the result in the interim data directory.
    """
    df = pd.read_csv(RAW_DIRECTORY / "data.csv")
    # Rename "locequip" column to "local"
    df.rename(columns={"locequip": "local"}, inplace=True)
    # Save the result in the interim data directory
    INTERIM_DIRECTORY.mkdir(parents=True, exist_ok=True)
    df.to_csv(INTERIM_DIRECTORY / "data.csv", index=False)


@task
def show_data() -> None:
    """
    Group by "bairro" column and show the top 5 neighborhoods with the most cameras.
    """
    df = pd.read_csv(INTERIM_DIRECTORY / "data.csv")
    print(df["bairro"].value_counts(sort=True).head(5))


@flow(log_prints=True)
def main():
    get_data(
        "https://raw.githubusercontent.com/prefeitura-rio/storage/refs/heads/master/camera_numero.csv"
    )
    transform_data()
    show_data()


if __name__ == "__main__":
    main()