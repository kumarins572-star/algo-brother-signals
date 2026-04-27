
import streamlit as st
import yfinance as yahoo

# 1. Page Configuration & Icon
st.set_page_config(
    page_title="Algo Brother Signals",
    page_icon="1777172501789.png",
    layout="wide"
)

# 2. Logo & Title
st.image("1777172501789.png", width=150)
st.title("Algo Brother Signals 📈")
st.write("Real-time Trading Signals for Crude Oil, Gold & Crypto")

# 3. Simple Dashboard Logic
symbol = st.selectbox("Select Asset", ["CL=F", "GC=F", "BTC-USD"])
data = yahoo.download(symbol, period="1d", interval="15m")

if not data.empty:
    st.line_chart(data['Close'])
    st.success(f"Current Price of {symbol}: ${data['Close'].iloc[-1]:.2f}")
else:
    st.error("Data loading... Please refresh.")
  
