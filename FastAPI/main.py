from fastapi import FastAPI, Query
from services import latest_coins, coin_by_name, get_history, top_gainers, top_losers

app = FastAPI(title="crypto_api")

@app.get("/latest")
def load_all_data():
    return latest_coins()

@app.get("/by_name")
def load_by_name(name: str):
    return coin_by_name(name)

@app.get("/names")
def get_all_names():
    data = latest_coins()
    names = [coin['name'] for coin in data]
    return {"names": names}

@app.get("/history")
def load_history(name: str = Query(...), hours: int = Query(100, ge=1, le=1000)):
    return get_history(name, hours)

@app.get("/top_gainers")
def load_top_gainers(limit: int = Query(10, ge=1, le=100)):
    return top_gainers(limit)

@app.get("/top_losers")
def load_top_losers(limit: int = Query(10, ge=1, le=100)):
    return top_losers(limit) 