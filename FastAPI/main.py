from fastapi import FastAPI, Query
from typing import List, Optional
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import snowflake.connector
import pandas as pd
import glob
import os

app = FastAPI(title="crypto_api")

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "crypto-data"
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")

@app.get("/latest")
def load_all_data():
    data = latest_coins()
    return data

def latest_coins():
    conn = snowflake_connection()
    try:
        query = conn.cursor().execute("""
                SELECT * FROM (
                SELECT * FROM COINS_DATA
                ORDER BY TO_TIMESTAMP_NTZ(LAST_UPDATED) DESC
                LIMIT 100
            )
            ORDER BY ID ASC
            """)
        data = query.fetchall()
        return data
    except Exception as e:
        return {"error": str(e)}

def snowflake_connection():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )
    conn.cursor().execute(f"USE DATABASE {database}")
    conn.cursor().execute(f"USE SCHEMA {schema}")
    return conn