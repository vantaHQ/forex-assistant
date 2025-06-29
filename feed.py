import requests
import pandas as pd

def get_ohlc_twelvedata(symbol="EUR/USD", interval="1min", apikey="YOUR_API_KEY"):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=500&apikey={apikey}&format=JSON"
    resp = requests.get(url)
    data = resp.json()["values"]
    df = pd.DataFrame(data)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df.sort_values("datetime")
