import requests
import pandas as pd
import os

from airflow.decorators import dag, task    
from pendulum import datetime
from azure.storage.blob import BlobServiceClient

header = {"header": os.getenv("COIN_GECKO_KEY")}
currency = "usd"
params = {"vs_currency": currency}
coins_url = "https://api.coingecko.com/api/v3/coins/markets"
azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

@dag(
    start_date=datetime(2025, 6, 20),
    schedule="0 * * * *",
    tags=["find"],
    catchup=False,
)

def find_activity():

    @task
    def get_coins():
        response = requests.get(coins_url, headers=header, params=params)
        return response.json()

    @task
    def clean_and_transform(data):

        df = pd.DataFrame(data)
        columns =[
            "name", "current_price", "price_change_24h", "price_change_percentage_24h",
            "high_24h", "low_24h", "market_cap", "market_cap_rank",
            "total_supply", "max_supply", "ath", "ath_change_percentage", "last_updated"
        ]
        df = df[columns]

        df["max_supply"] = df["max_supply"].replace("Unknown", None)
        df["max_supply"] = pd.to_numeric(df["max_supply"], errors="coerce")

        df["relative_to_ath"] = df["current_price"] / df["ath"]

        df["variation_percent"] = df["price_change_24h"] / (df["current_price"] - df["price_change_24h"]) * 100
        print(df.head())
        return df.to_dict(orient="records")
    
    @task
    def to_parquet(data, ts=None):
        df = pd.DataFrame(data)
        filename = f"coins_data_{ts}.csv"
        df.to_csv(filename)
        return filename

    @task
    def connect_to_azure_blob(parquet_file, ts=None):
        service_client = BlobServiceClient.from_connection_string(azure_connection_string)
        container_name = "crypto-data"
        blob_path = f"history/{ts}/{parquet_file}"
        container_client = service_client.get_container_client(container_name)
    
        blob_object = service_client.get_blob_client(container=container_name, blob=blob_path)
        with open(parquet_file, "rb") as data:
            blob_object.upload_blob(data)

    raw_data = get_coins()
    cleaned_data = clean_and_transform(raw_data)
    parquet_file = to_parquet(cleaned_data, ts = "{{ ts_nodash }}")
    connect_to_azure_blob(parquet_file, ts = "{{ ds_nodash }}")
    
find_activity()