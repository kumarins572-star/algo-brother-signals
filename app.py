import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Algo Brother Signals",
    page_icon="1777172501789.png",
    layout="wide"
)

# 2. Logo & Title
try:
    st.image("1777172501789.png", width=150)
except:
    st.title("🚀 Algo Brother Signals")

st.title("Algo Brother Signals 📈")
st.write("Real-time Trading Signals for Crude Oil")

# 3. Dashboard Logic
symbol = st.selectbox("Select Asset", ["CL=F", "GC=F", "BTC-USD"])

# Placeholder areas for live updates
open_box, high_box, low_box, close_box = st.columns(4)
o_metric = open_box.empty()
h_metric = high_box.empty()
l_metric = low_box.empty()
c_metric = close_box.empty()

signal_area = st.empty()

# 4. Automation Loop
def fetch_data():
    # Fetching 1-day data with 2m intervals (for 3m/5m analysis)
    df = yf.download(symbol, period="1d", interval="2m")
    if df.empty:
        return None
    
    # Calculate RSI
    df['RSI'] = ta.rsi(df['Close'], length=14)
    return df

# Start the live process
while True:
    data = fetch_data()
    
    if data is not None:
        last_row = data.iloc[-1]
        o, h, l, c = last_row['Open'], last_row['High'], last_row['Low'], last_row['Close']
        rsi_val = last_row['RSI']
        
        # Automatic OHLC Update
        o_metric.metric("Open", f"{o:.2f}")
        h_metric.metric("High", f"{h:.2f}")
        l_metric.metric("Low", f"{l:.2f}")
        c_metric.metric("Close", f"{c:.2f}")
        
        # Logic for Normal Signal and Confirm Alarm
        body = abs(c - o)
        lower_wick = min(o, c) - l
        is_hammer = lower_wick > (2 * body)
        
        if rsi_val < 35:
            if is_hammer:
                signal_area.success("🔔 ALARM: BUY CANDLE STICK CONFIRM BUY!")
                st.toast("BUY CONFIRMED!")
            else:
                signal_area.warning("STATUS: Normal Buy - Waiting for Candle Confirmation")
        else:
            signal_area.info("STATUS: Scanning Market... Wait")
            
    time.sleep(10) # Refresh every 10 seconds
