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
start_date = "2005-01-01"  # Unified start date

# ========== FUNCTIONS ========== #

def fetch_macro_data():
    print("Fetching macroeconomic data from FRED...")
    macro_data = {}
    for name, code in macro_series.items():
        series = fred.get_series(code)
        macro_data[name] = series.loc[start_date:]  # Filter to match asset price range
    df = pd.DataFrame(macro_data)
    df.index.name = "Date"
    df = df.resample('ME').ffill()  # Monthly end
    df.to_csv("data/macro_data.csv")
    print("Saved macro data to data/macro_data.csv")


def fetch_asset_prices():
    print("Fetching asset price data from Yahoo Finance...")
    all_data = {}

    for ticker in asset_tickers:
        try:
            print(f"Fetching: {ticker}")
            df = yf.download(ticker, start=start_date, end="2024-12-31", interval="1d", auto_adjust=True)
            if df.empty:
                print(f"No data found for {ticker}, skipping.")
                continue

            df = df[['Close']].resample("ME").ffill()
            df.columns = [ticker]  # Rename column to ticker name
            all_data[ticker] = df

            print(f"✅ {ticker} data range: {df.index.min().date()} to {df.index.max().date()}")

        except Exception as e:
            print(f"❌ Failed to fetch {ticker}: {e}")

    if not all_data:
        raise ValueError("No valid asset data retrieved. Please check tickers or date range.")

    prices_df = pd.concat(all_data.values(), axis=1)
    prices_df.index.name = "Date"
    prices_df.to_csv("data/asset_prices.csv")
    print("✅ Saved asset prices to data/asset_prices.csv")


# ========== MAIN EXECUTION ========== #
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    fetch_macro_data()
    fetch_asset_prices()
