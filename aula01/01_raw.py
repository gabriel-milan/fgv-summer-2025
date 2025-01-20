import pandas as pd
import requests


def get_data(csv_url: str) -> None:
    """
    Function to get data. Downloads the CSV file from the URL into the current directory.
    """
    response = requests.get(csv_url)
    with open("data/raw/data.csv", "wb") as file:
        file.write(response.content)


def transform_data() -> None:
    """
    Function to transform data. Reads the CSV file from the raw data directory, perform some
    transformations and saves the result in the interim data directory.
    """
    df = pd.read_csv("data/raw/data.csv")
    # Rename "locequip" column to "local"
    df.rename(columns={"locequip": "local"}, inplace=True)
    # Save the result in the interim data directory
    df.to_csv("data/interim/data.csv", index=False)


def show_data() -> None:
    """
    Group by "bairro" column and show the top 5 neighborhoods with the most cameras.
    """
    df = pd.read_csv("data/interim/data.csv")
    print(df["bairro"].value_counts(sort=True).head(5))

if __name__ == "__main__":
    get_data(
        "https://raw.githubusercontent.com/prefeitura-rio/storage/refs/heads/master/camera_numero.csv"
    )
    transform_data()
    show_data()
