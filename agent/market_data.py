import requests
from datetime import datetime, timedelta

def get_stock_weekly_change(ticker: str) -> dict:
    """Fetch weekly price change for a ticker via Yahoo Finance"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "7d"
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        closes = [c for c in closes if c is not None]

        if len(closes) < 2:
            return {"value": "N/A", "change": "N/A", "direction": "flat"}

        start = closes[0]
        end = closes[-1]
        change_pct = ((end - start) / start) * 100

        return {
            "value": f"${end:.2f}",
            "change": f"{change_pct:+.1f}%",
            "direction": "up" if change_pct > 0 else "down"
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return {"value": "N/A", "change": "N/A", "direction": "flat"}


def get_market_snapshot() -> dict:
    """Fetch all three header metrics"""
    print("  Fetching market data...")

    rcl = get_stock_weekly_change("RCL")
    sp500 = get_stock_weekly_change("^GSPC")
    crude = get_stock_weekly_change("CL=F")

    return {
        "rcl_price": rcl["value"],
        "rcl_change": rcl["change"],
        "rcl_direction": rcl["direction"],
        "sp500_change": sp500["change"],
        "sp500_direction": sp500["direction"],
        "crude_change": crude["change"],
        "crude_direction": crude["direction"],
        "crude_price": crude["value"]
    }