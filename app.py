import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="تحليل الذهب - Fintech Cyberpunk", page_icon="📈")

st.title("تحليل الذهب اليومي – Fintech Cyberpunk ⚡️")
st.markdown("بوت بسيط لتحليل XAUUSD – مجاني 100%")

@st.cache_data(ttl=300)  # refresh كل 5 دقائق
def get_gold_data():
    return yf.download('GC=F', period="3mo", interval="1d")

data = get_gold_data()

if data.empty:
    st.error("مشكلة في جلب البيانات، جرب لاحقًا أو تحقق من الإنترنت")
else:
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()
    
    current_price = data['Close'].iloc[-1]
    ema50 = data['EMA50'].iloc[-1]
    ema200 = data['EMA200'].iloc[-1]
    
    if current_price > ema50 > ema200:
        bias = "صاعد قوي (Bullish Strong)"
        color = "green"
    elif current_price > ema50:
        bias = "صاعد (Bullish)"
        color = "lime"
    elif current_price < ema50 < ema200:
        bias = "هابط قوي (Bearish Strong)"
        color = "red"
    else:
        bias = "جانبي / غير واضح"
        color = "orange"
    
    recent = data.tail(10)
    support = recent['Low'].min()
    resistance = recent['High'].max()
    
    st.subheader("النتيجة الحالية:")
    st.metric("سعر الذهب الحالي", f"{current_price:.2f} $")
    
    st.markdown(f"**الاتجاه**: <span style='color:{color}; font-weight:bold; font-size:1.3em;'>{bias}</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("EMA 50", f"{ema50:.2f}")
    col2.metric("EMA 200", f"{ema200:.2f}")
    
    col3, col4 = st.columns(2)
    col3.metric("دعم قريب", f"{support:.2f}")
    col4.metric("مقاومة قريبة", f"{resistance:.2f}")

st.markdown("---")
st.caption("Powered by yfinance • تحديث كل بضع دقائق • تابع @fintech.cyberpunk على TikTok")
