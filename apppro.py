

import streamlit as st
import pandas as pd
from analysis import fetch_data, add_indicators, performance_summary
from utils import export_csv
import plotly.graph_objects as go


def main():
    st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
    st.title("Stock Analysis Dashboard")

    st.sidebar.header("Settings")
    ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    data = fetch_data(ticker, start_date, end_date)
    if data.empty:
        st.warning("No data found. Please check the ticker symbol or date range.")
        return

    data = add_indicators(data)

    st.subheader(f"Raw Data – {ticker}")
    st.dataframe(data.tail())

    st.subheader("Candlestick Chart")
    candle = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    candle.update_layout(xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(candle, use_container_width=True)

    st.subheader("Close Price with SMA & EMA")
    line = go.Figure()
    line.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close"))
    line.add_trace(go.Scatter(x=data.index, y=data["SMA_20"], name="SMA 20"))
    line.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], name="EMA 20"))
    line.update_layout(height=500)
    st.plotly_chart(line, use_container_width=True)

    st.subheader("Relative Strength Index (RSI)")
    rsi_chart = go.Figure()
    rsi_chart.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI"))
    rsi_chart.update_layout(height=300, yaxis=dict(range=[0, 100]))
    st.plotly_chart(rsi_chart, use_container_width=True)

    st.subheader("Performance Summary")
    summary = performance_summary(data)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Return (%)", summary["Total Return (%)"])
    col2.metric("Highest Price", summary["Highest Price"])
    col3.metric("Lowest Price", summary["Lowest Price"])
    
    st.subheader("Download Data")
    csv = export_csv(data, f"{ticker}_data.csv")
    st.download_button("Download CSV", csv, f"{ticker}_data.csv", "text/csv")


if __name__ == "__main__":
    main()
