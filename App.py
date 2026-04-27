import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from streamlit_autorefresh import st_autorefresh

# ================= CONFIG =================
st.set_page_config(page_title="Algo Brother Signals", page_icon="📈", layout="wide")

# Auto refresh (10 sec)
st_autorefresh(interval=10000, key="refresh")

# ================= HEADER =================
try:
    st.image("1777172501789.png", width=120)
except:
    st.title("🚀 ALGO BROTHER SIGNALS")

st.write("---")

# ================= SYMBOL =================
symbol = "CL=F"
st.subheader(f"🔴 Live Terminal: {symbol}")

# ================= UI =================
col1, col2, col3, col4 = st.columns(4)
o_metric = col1.empty()
h_metric = col2.empty()
l_metric = col3.empty()
c_metric = col4.empty()

status_area = st.empty()

# ================= DATA FETCH =================
@st.cache_data(ttl=8)
def load_data(sym):
    df = yf.download(sym, period="1d", interval="2m", progress=False)
    return df

try:
    df = load_data(symbol)

    if df is not None and not df.empty:

        # ===== LAST CANDLE =====
        last = df.iloc[-1]
        o, h, l, c = last['Open'], last['High'], last['Low'], last['Close']

        # ===== DISPLAY =====
        o_metric.metric("Open", f"{o:.2f}")
        h_metric.metric("High", f"{h:.2f}")
        l_metric.metric("Low", f"{l:.2f}")
        c_metric.metric("Close", f"{c:.2f}")

        # ===== INDICATORS =====
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA50'] = ta.ema(df['Close'], length=50)

        rsi_val = df['RSI'].iloc[-1]
        ema_val = df['EMA50'].iloc[-1]

        st.markdown(f"**RSI:** `{round(rsi_val,2)}` | **EMA50:** `{round(ema_val,2)}`")

        # ===== CANDLE LOGIC =====
        body = abs(c - o)
        lower_wick = min(o, c) - l
        upper_wick = h - max(o, c)

        # Avoid divide/false signals
        if body == 0:
            body = 0.0001

        is_hammer = lower_wick > (2 * body) and upper_wick < body
        is_shooting_star = upper_wick > (2 * body) and lower_wick < body

        st.write("---")

        # ===== SIGNAL ENGINE =====
        if rsi_val < 35 and c > ema_val:
            if is_hammer:
                status_area.success("🚀 STRONG BUY SIGNAL (RSI + EMA + HAMMER)")
                st.toast("BUY CONFIRMED")
            else:
                status_area.warning("⚠️ Buy Zone - Waiting for Hammer")

        elif rsi_val > 65 and c < ema_val:
            if is_shooting_star:
                status_area.error("📉 STRONG SELL SIGNAL (RSI + EMA + SHOOTING STAR)")
                st.toast("SELL CONFIRMED")
            else:
                status_area.warning("⚠️ Sell Zone - Waiting for Shooting Star")

        else:
            status_area.info("⌛ Market Neutral...")

    else:
        st.warning("⚠️ No market data received")

except Exception as e:
    st.error(f"❌ System Error: {e}")
