# src/data_loader.py

import pandas as pd
import yfinance as yf
from fredapi import Fred
import os

# ========== CONFIG ========== #
FRED_API_KEY = "423712ffba83cf65975542f987667a3a"
fred = Fred(api_key=FRED_API_KEY)

macro_series = {
    'US_CPI': 'CPIAUCNS',
    'US_FED_FUNDS_RATE': 'FEDFUNDS',
    'US_10Y_YIELD': 'GS10',
    'EURO_AREA_CPI': 'CP0000EZ19M086NEST',
    'GERMANY_3M_RATE': 'IR3TIB01DEM156N'
}

asset_tickers = ['SPY', 'EWG', 'FXE', 'EURUSD=X']  # US ETF, Germany ETF, Euro ETF, EUR/USD FX

# ========== FUNCTIONS ========== #

def fetch_macro_data():
    print("Fetching macroeconomic data from FRED...")
    macro_data = {}
    for name, code in macro_series.items():
        macro_data[name] = fred.get_series(code)
    df = pd.DataFrame(macro_data)
    df.index.name = "Date"
    df = df.resample('ME').ffill()
    df.to_csv("data/macro_data.csv")
    print("Saved macro data to data/macro_data.csv")


def fetch_asset_prices():
    print("Fetching asset price data from Yahoo Finance...")
    all_data = {}

    for ticker in asset_tickers:
        try:
            print(f"Fetching: {ticker}")
            df = yf.Ticker(ticker).history(start="2010-01-01", interval="1d")['Close']
            df = df.resample("ME").ffill()
            all_data[ticker] = df.rename(ticker)
        except Exception as e:
            print(f"Failed to fetch {ticker}: {e}")

    prices_df = pd.concat(all_data.values(), axis=1)
    prices_df.to_csv("data/asset_prices.csv")
    print("Saved asset prices to data/asset_prices.csv")

# ========== MAIN EXECUTION ========== #
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    fetch_macro_data()
    fetch_asset_prices()
 
