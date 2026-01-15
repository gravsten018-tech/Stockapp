import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ------------------------------
# App Configuration
# ------------------------------
st.set_page_config(
    page_title="Stock Market Visualiser",
    layout="wide"
)

st.title("📈 Stock Market Visualiser")
st.markdown("Analyze and visualize stock market data using **yfinance**.")

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("User Input")

ticker = st.sidebar.text_input(
    "Stock Ticker",
    value="AAPL",
    help="Example: AAPL, TSLA, MSFT"
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2022-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date.today()
)

# ------------------------------
# Fetch Stock Data
# ------------------------------
@st.cache_data
def load_data(ticker, start, end):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start, end=end)
    return stock, df

try:
    stock, df = load_data(ticker, start_date, end_date)

    if df.empty:
        st.error("No data found. Please check the ticker symbol.")
        st.stop()

    # ------------------------------
    # Company Info
    # ------------------------------
    info = stock.info

    st.subheader(f"🏢 {info.get('longName', ticker)}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Sector", info.get("sector", "N/A"))
    col2.metric("Market Cap", f"${info.get('marketCap', 0):,}")
    col3.metric("Country", info.get("country", "N/A"))

    # ------------------------------
    # Moving Averages
    # ------------------------------
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # ------------------------------
    # Price Chart
    # ------------------------------
    st.subheader("📊 Closing Price & Moving Averages")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df["Close"], label="Close Price", linewidth=2)
    ax.plot(df.index, df["MA20"], label="20-Day MA", linestyle="--")
    ax.plot(df.index, df["MA50"], label="50-Day MA", linestyle="--")

    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # ------------------------------
    # Volume Chart
    # ------------------------------
    st.subheader("📉 Trading Volume")

    fig2, ax2 = plt.subplots(figsize=(12, 4))
    ax2.bar(df.index, df["Volume"], color="orange")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Volume")
    ax2.grid(True)

    st.pyplot(fig2)

    # ------------------------------
    # Raw Data
    # ------------------------------
    with st.expander("📄 View Raw Data"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Something went
