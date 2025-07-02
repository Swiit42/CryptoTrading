# 🪙 Crypto Dashboard – Suivi en temps réel avec Airflow, Snowflake, Azure et Streamlit

## 📌 Description

Ce projet est un tableau de bord complet permettant de **suivre en temps réel l'évolution des crypto-monnaies**. Il repose sur un **pipeline de données automatisé**, une **API REST**, et une interface visuelle via **Streamlit**.

---

## 🔧 Architecture du projet

### 🔀 1. **Collecte de données (Airflow + CoinGecko)**

* Les données sont récupérées toutes les heures depuis l'API de [CoinGecko](https://www.coingecko.com/fr/api).
* Les données brutes sont nettoyées, enrichies (calculs comme la variation en pourcentage), puis sauvegardées.

### ☁️ 2. **Stockage**

* **Azure Blob Storage** : archive les snapshots horaires sous forme de fichiers CSV.
* **Snowflake** : stocke les données tabulaires pour permettre les requêtes en temps réel (derniers prix, historiques, top variations…).

### 🚀 3. **API FastAPI**

Une API REST est exposée pour interagir avec les données stockées dans Snowflake :

* `/latest` : les dernières données crypto
* `/by_name` : historique d’une crypto
* `/top_gainers` / `/top_losers` : meilleures hausses ou baisses sur 24h
* `/history` : historique glissant sur X heures

### 📊 4. **Dashboard (Streamlit)**

L’application Streamlit permet de :

* Visualiser les dernières cryptos ajoutées
* Afficher les plus fortes hausses et baisses du marché
* Explorer l’historique d’une crypto sur 1 jour, 7 jours, ou 30 jours

---

## ⚙️ Technologies utilisées

| Composant              | Rôle                             |
| ---------------------- | -------------------------------- |
| **Airflow**            | Orchestration horaire des tâches |
| **CoinGecko API**      | Source de données crypto         |
| **Pandas**             | Nettoyage et transformation      |
| **Azure Blob Storage** | Stockage d’archives              |
| **Snowflake**          | Base de données analytique       |
| **FastAPI**            | API REST                         |
| **Streamlit**          | Dashboard interactif             |

---

## 📁 Organisation du code

* `airflow_dag.py` : collecte, transformation et stockage des données
* `services.py` : fonctions de requête vers Snowflake
* `main.py` (FastAPI) : routes API exposées
* `streamlit_app.py` : dashboard final
* `.env` : variables de configuration (Snowflake, Azure, etc.)

---

## 🚀 Lancer le projet localement

### 1. Lancer l’API :

```bash
uvicorn main:app --reload
```

### 2. Lancer le dashboard :

```bash
streamlit run streamlit_app.py
```
