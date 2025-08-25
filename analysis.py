import yfinance as yf
import pandas as pd
import ta


def fetch_data(ticker: str, start, end) -> pd.DataFrame:
    """
    Download historical stock data from Yahoo Finance.
    """
    try:
        df = yf.download(ticker, start=start, end=end)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add common technical indicators (SMA, EMA, RSI).
    """
    if df.empty:
        return df

    df["SMA_20"] = ta.trend.sma_indicator(df["Close"], window=20)

    df["EMA_20"] = ta.trend.ema_indicator(df["Close"], window=20)

    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

    return df


def performance_summary(df: pd.DataFrame) -> dict:
    """
    Return basic performance metrics for the stock.
    """
    if df.empty:
        return {
            "Total Return (%)": None,
            "Highest Price": None,
            "Lowest Price": None,
        }

    start_price = df["Close"].iloc[0]
    end_price = df["Close"].iloc[-1]
    total_return = ((end_price - start_price) / start_price) * 100

    summary = {
        "Total Return (%)": round(total_return, 2),
        "Highest Price": round(df["High"].max(), 2),
        "Lowest Price": round(df["Low"].min(), 2),
    }

    return summary
