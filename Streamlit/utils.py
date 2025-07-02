import pandas as pd
import streamlit as st

import requests

API_URL = "http://localhost:8000"

@st.cache_data
def get_latest_data():
    response = requests.get(f"{API_URL}/latest")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Erreur lors de la récupération des données")
        return pd.DataFrame()

@st.cache_data
def get_all_names():
    names = requests.get(f"{API_URL}/names")
    return sorted(names.json()["names"]) if names.status_code == 200 else []

def get_top_gainers(limit: int = 10):
    gainers = requests.get(f"{API_URL}/top_gainers", params={"limit": limit}).json()
    print(gainers)
    return pd.DataFrame(gainers)

def get_top_losers(limit: int = 10):
    losers = requests.get(f"{API_URL}/top_losers", params={"limit": limit}).json()
    return pd.DataFrame(losers)

def get_history(name: str, limit: int = 100):
    history_all = requests.get(f"{API_URL}/history", params={"name": name, "limit": limit}).json()
    return pd.DataFrame(history_all)

def color_change(df):
    if df is None or df.empty:
        return df

    df.columns = [prettify(c) for c in df.columns]

    styled = df.style

    change_cols = [col for col in df.columns if "change" in col.lower()]
    styled = styled.applymap(color, subset=change_cols)

    if "Current price" in df.columns:
        styled = styled.format({
            "Current price": lambda x: "—" if x == 0 else f"{x:,.2f} $"
        })

    return styled


def color(val):
        try:
            val = float(val)
            if val > 0:
                return "color: green"
            elif val < 0:
                return "color: red"
        except:
            return ""
        return ""

def prettify(col):
    return col.replace("_", " ").capitalize()