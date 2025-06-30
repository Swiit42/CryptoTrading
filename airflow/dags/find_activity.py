from airflow.decorators import dag, task    
from pendulum import datetime

import requests
import pandas as pd
import os

from azure.storage.blob import BlobServiceClient

api_key = "CG-3nRHfUKnVkSGBTeEVkm9Shrw"
header = {"header":api_key}
currency = "usd"
params = {"vs_currency": currency}
coins_url = "https://api.coingecko.com/api/v3/coins/markets"
azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

@dag(
    start_date=datetime(2025, 6, 20),
    schedule="@daily",
    tags=["find"],
    catchup=False,
)
def find_activity():

    @task
    def get_coins():
        response = requests.get(coins_url, headers=header, params=params)
        return response.json()
    get_coins()

find_activity()