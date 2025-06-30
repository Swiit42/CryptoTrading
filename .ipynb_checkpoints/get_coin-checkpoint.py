import requests
import pandas as pd

# Prepate coingecko request

api_key = "CG-3nRHfUKnVkSGBTeEVkm9Shrw"
header = {"header":api_key}
currency = "usd"
params = {"vs_currency": currency}
coins_url = "https://api.coingecko.com/api/v3/coins/markets"

# Make request 
req = requests.get(url = coins_url, headers= header, params=params)
data = req.json()
df = pd.DataFrame(data)

# Clean data
colonnes = ["name", "image", "current_price", "price_change_24h", "price_change_percentage_24h", "high_24h", "low_24h", "market_cap", "market_cap_rank", "total_supply", "max_supply", "ath", "ath_change_percentage", "last_updated"]
df = df[colonnes]
df["max_supply"] = df["max_supply"].fillna("Unknown")
df.head()
