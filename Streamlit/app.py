import streamlit as st
import pandas as pd
import requests
from utils import get_latest_data, get_all_names, prettify, get_top_gainers, get_top_losers, get_history, color_change, API_URL

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("Crypto Trade")
st.sidebar.title("Filtres")

df = get_latest_data()

default_cols = ["name", "current_price", "price_change_percentage_24h"]
columns_to_show = []

# Sidebar
selected_name = st.sidebar.selectbox("Sélectionne une crypto", get_all_names())
period = st.sidebar.selectbox("Période", ["1 jour", "7 jours", "30 jours"])
period_to_hours = {"1 jour": 24, "7 jours": 168, "30 jours": 720}
nb_hours = period_to_hours[period]
st.sidebar.subheader("Colonnes à afficher")

for col in df.columns:
    if col == "id":
        continue
    label = prettify(col)
    show = st.sidebar.checkbox(label, value=(col in default_cols))
    if show:
        columns_to_show.append(col)

tabs = st.tabs(["Derniers ajouts", "Top évolutions", "Historique complet"])

with tabs[0]:
    st.subheader("Derniers ajouts")
    if not df.empty:
        st.table(color_change(df[columns_to_show]))
        st.write(f"Dernière mise à jour : {pd.to_datetime(df['last_updated'].max()).strftime('%H:%M %Y-%m-%d')}")
    else:
        st.warning("Aucune donnée à afficher.")

with tabs[1]:
    st.subheader("Top hausses 24h")
    df_gainers = get_top_gainers()
    st.dataframe(color_change(df_gainers[columns_to_show]))

    st.subheader("Top baisses 24h")
    df_losers = get_top_losers()
    st.dataframe(color_change(df_losers[columns_to_show]))


with tabs[2]:
    st.subheader(f"Historique global : {selected_name}")
    st.write(f"Historique de {selected_name} sur {period}")
    df_all = get_history(selected_name, period_to_hours[period])
    df_all["Last updated"] = pd.to_datetime(df_all["last_updated"])
    df_chart = df_all.sort_values("Last updated")
    st.line_chart(data=df_chart, x="Last updated", y='current_price', use_container_width=True)
    st.dataframe(color_change(df_all[columns_to_show]))
    