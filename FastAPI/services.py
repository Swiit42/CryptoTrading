import snowflake.connector
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "crypto-data"
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")

def latest_coins():
    query = """ SELECT * FROM (
                SELECT * FROM COINS_DATA
                ORDER BY TO_TIMESTAMP_NTZ(LAST_UPDATED) DESC
                LIMIT 100
            ) ORDER BY ID ASC """
    return fetch_query(query)


def coin_by_name(name: str):
    query = """SELECT * FROM COINS_DATA
            WHERE LOWER(NAME) = LOWER(%s)
            ORDER BY TO_TIMESTAMP_NTZ(LAST_UPDATED) DESC
            LIMIT 100
        """
    params = (name,)
    return fetch_query(query , params)

def top_coins(limit: int = 10):
    query = f"""SELECT * FROM COINS_DATA
        WHERE TO_TIMESTAMP_NTZ(LAST_UPDATED) = (
        SELECT MAX(TO_TIMESTAMP_NTZ(LAST_UPDATED)) FROM COINS_DATA
        )
        ORDER BY price_change_percentage_24h DESC
        LIMIT (%s)""", 
    params = (limit,)
    return fetch_query(query, params)

def get_history(name: str, limit: int = 100):
    query = """SELECT * FROM COINS_DATA
            WHERE LOWER(NAME) = LOWER(%s)
            ORDER BY TO_TIMESTAMP_NTZ(LAST_UPDATED) DESC
            LIMIT %s"""
    params = (name, limit)
    return fetch_query(query, params)

def top_gainers(limit: int = 10):
    sql = """
        SELECT * FROM COINS_DATA
        WHERE TO_TIMESTAMP_NTZ(LAST_UPDATED) = (
            SELECT MAX(TO_TIMESTAMP_NTZ(LAST_UPDATED)) FROM COINS_DATA
        )
        ORDER BY price_change_percentage_24h DESC
        LIMIT %s
    """
    params = (limit,)
    return fetch_query(sql, params)

def top_losers(limit: int = 10):
    sql = """
        SELECT * FROM COINS_DATA
        WHERE TO_TIMESTAMP_NTZ(LAST_UPDATED) = (
            SELECT MAX(TO_TIMESTAMP_NTZ(LAST_UPDATED)) FROM COINS_DATA
        )
        ORDER BY price_change_percentage_24h ASC
        LIMIT %s
    """
    params = (limit,)
    return fetch_query(sql, params)

    
def map_rows_to_dicts(rows):
    column_names = [
        "id", "ath", "name", "low_24h", "high_24h", "market_cap", "max_supply",
        "last_updated", "total_supply", "current_price", "market_cap_rank",
        "relative_to_ath", "price_change_24h", "variation_percent",
        "ath_change_percentage", "price_change_percentage_24h"
    ]
    return [dict(zip(column_names, row)) for row in rows]

def fetch_query(query: str, params=None):
    conn = snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return map_rows_to_dicts(cursor.fetchall())
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