import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from streamlit_autorefresh import st_autorefresh

# 1. LINE 1: Logo & Auto-Refresh (Every 10 Seconds)
st_autorefresh(interval=10000, key="datarefresh")
st.set_page_config(page_title="Algo Brother Signals", page_icon="📈", layout="wide")

try:
    st.image("1777172501789.png", width=120)
except:
    st.title("🚀 ALGO BROTHER SIGNALS")

# 2. LINE 1 & 4: Asset & Automated OHLC Monitoring
symbol = "CL=F" # Crude Oil Benchmark
st.subheader(f"🔴 Live Terminal: {symbol}")

# UI Layout for OHLC Boxes (Automatically filled)
col1, col2, col3, col4 = st.columns(4)
o_metric = col1.empty()
h_metric = col2.empty()
l_metric = col3.empty()
c_metric = col4.empty()

status_area = st.empty()

try:
    # 3. LINE 2: Auto-Scan (3m/5m equivalent)
    df = yf.download(symbol, period="1d", interval="2m")

    if not df.empty:
        last = df.iloc[-1]
        o, h, l, c = last['Open'], last['High'], last['Low'], last['Close']

        # Update OHLC Boxes Automatically
        o_metric.metric("Open", f"{o:.2f}")
        h_metric.metric("High", f"{h:.2f}")
        l_metric.metric("Low", f"{l:.2f}")
        c_metric.metric("Close", f"{c:.2f}")

        # 4. Technical Indicator Engine (RSI & EMA)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        
        rsi_val = df['RSI'].iloc[-1]
        ema_val = df['EMA50'].iloc[-1]

        st.markdown(f"**Current RSI:** `{round(rsi_val,2)}` | **EMA 50:** `{round(ema_val,2)}`")

        # 5. LINE 4: Automatic Candle Pattern Math
        body = abs(c - o)
        lower_wick = min(o, c) - l
        upper_wick = h - max(o, c)

        is_hammer = lower_wick > (2 * body) and upper_wick < (body * 0.5)
        is_shooting_star = upper_wick > (2 * body) and lower_wick < (body * 0.5)

        # 6. LINE 3, 5, 6 & 7: The Master Signal Logic
        st.write("---")
        
        # BUY LOGIC
        if rsi_val < 35 and c > ema_val:
            if is_hammer:
                # LINE 7: Final Output Alert
                st.success("🔔 ALARM: BUY CANDLE STICK CONFIRM BUY! 🚀")
                st.balloons() # Visual Notification
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)
            else:
                # LINE 3: Normal Signal Alert
                st.warning("⚠️ STATUS: Normal Buy Alert (RSI/Trend) - Waiting for Hammer Confirmation...")

        # SELL LOGIC
        elif rsi_val > 65 and c < ema_val:
            if is_shooting_star:
                # LINE 7: Final Output Alert
                st.error("🔔 ALARM: SELL CANDLE STICK CONFIRM SELL! 📉")
                st.snow() # Visual Notification
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)
            else:
                # LINE 3: Normal Signal Alert
                st.warning("⚠️ STATUS: Normal Sell Alert (RSI/Trend) - Waiting for Shooting Star Confirmation...")

        # LINE 5: Neutral State
        else:
            st.info("⌛ TOTAL ALARM: WAIT (Scanning for high-probability setup...)")

    else:
        st.warning("Waiting for Market Data Connection...")

except Exception as e:
    st.error(f"System Error: {e}")
    
