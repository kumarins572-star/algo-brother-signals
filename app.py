
import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# 1. Page Branding
st.set_page_config(page_title="Algo Brother Signals", page_icon="📈", layout="wide")

try:
    st.image("1777172501789.png", width=120)
except:
    st.title("🚀 ALGO BROTHER SIGNALS")

st.write("---")

# 2. Market Data Detection (Crude Oil)
symbol = "CL=F"
st.subheader(f"🔴 Live Terminal: {symbol}")

# UI Layout for OHLC Metrics
col1, col2, col3, col4 = st.columns(4)
o_box = col1.empty()
h_box = col2.empty()
l_box = col3.empty()
c_box = col4.empty()

try:
    # 3. Fetch Live Data
    df = yf.download(symbol, period="1d", interval="2m")

    # Fix yfinance MultiIndex columns issue
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    if not df.empty:
        last = df.iloc[-1]
        o, h, l, c = last['Open'], last['High'], last['Low'], last['Close']

        # 4. Technical Indicators using 'ta' library
        df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
        df['EMA50'] = ta.trend.EMAIndicator(close=df['Close'], window=50).ema_indicator()
        
        rsi_val = df['RSI'].iloc[-1]
        ema_val = df['EMA50'].iloc[-1]

        # Update Display Boxes
        o_box.metric("Open", f"{o:.2f}")
        h_box.metric("High", f"{h:.2f}")
        l_box.metric("Low", f"{l:.2f}")
        c_box.metric("Close", f"{c:.2f}")

        st.markdown(f"**RSI:** `{round(rsi_val,2)}` | **EMA 50:** `{round(ema_val,2)}`")

        # 5. Candle Pattern Logic
        body = abs(c - o)
        lower_wick = min(o, c) - l
        upper_wick = h - max(o, c)

        is_hammer = lower_wick > (2 * body) and upper_wick < (body * 0.5) and body > 0
        is_shooting_star = upper_wick > (2 * body) and lower_wick < (body * 0.5) and body > 0

        # 6. Final Output & Alerts
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
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ STATUS: Sell Alert - Waiting for Shooting Star Confirmation...")

        else:
            st.info("⌛ TOTAL ALARM: WAIT (Market Neutral...)")

except Exception as e:
    st.error(f"System Error: {e}")
