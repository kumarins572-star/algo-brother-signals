import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from streamlit_autorefresh import st_autorefresh

# 1. Automatic Refresh every 10 seconds
st_autorefresh(interval=10000, key="datarefresh")

# 2. Page Setup
st.set_page_config(page_title="Algo Brother Signals", page_icon="📈", layout="wide")

# 3. Logo and Branding
try:
    st.image("1777172501789.png", width=120)
except:
    st.title("🚀 ALGO BROTHER SIGNALS")

st.write("---")

# 4. Asset Selection (Crude Oil)
symbol = "CL=F"
st.subheader(f"🔴 Live Terminal: {symbol}")

# UI for OHLC Display
col1, col2, col3, col4 = st.columns(4)
o_metric = col1.empty()
h_metric = col2.empty()
l_metric = col3.empty()
c_metric = col4.empty()

try:
    # 5. Fetch Real-Time Data
    df = yf.download(symbol, period="1d", interval="2m")

    if not df.empty:
        last = df.iloc[-1]
        o, h, l, c = last['Open'], last['High'], last['Low'], last['Close']

        # 6. Technical Indicators (RSI & EMA)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        
        rsi_val = df['RSI'].iloc[-1]
        ema_val = df['EMA50'].iloc[-1]

        # 7. Update Live Boxes
        o_metric.metric("Open", f"{o:.2f}")
        h_metric.metric("High", f"{h:.2f}")
        l_metric.metric("Low", f"{l:.2f}")
        c_metric.metric("Close", f"{c:.2f}")

        st.markdown(f"**RSI:** `{round(rsi_val,2)}` | **EMA 50:** `{round(ema_val,2)}`")

        # 8. Candle Pattern Logic
        body = abs(c - o)
        lower_wick = min(o, c) - l
        upper_wick = h - max(o, c)

        is_hammer = lower_wick > (2 * body) and upper_wick < (body * 0.5)
        is_shooting_star = upper_wick > (2 * body) and lower_wick < (body * 0.5)

        # 9. Master Signal Logic
        st.write("---")
        
        if rsi_val < 35 and c > ema_val:
            if is_hammer:
                st.success("🔔 ALARM: BUY CANDLE STICK CONFIRM BUY! 🚀")
                st.balloons()
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ STATUS: Buy Alert - Waiting for Hammer Confirmation...")

        elif rsi_val > 65 and c < ema_val:
            if is_shooting_star:
                st.error("🔔 ALARM: SELL CANDLE STICK CONFIRM SELL! 📉")
                st.snow()
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio
              
