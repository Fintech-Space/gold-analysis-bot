import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np  # للتعامل مع NaN بشكل أفضل

st.set_page_config(page_title="تحليل الذهب - Fintech Cyberpunk", page_icon="📈")

st.title("تحليل الذهب اليومي – Fintech Cyberpunk ⚡️")
st.markdown("بوت بسيط لتحليل XAUUSD – مجاني 100%")

@st.cache_data(ttl=900)  # تحديث كل 15 دقيقة
def get_gold_data():
    try:
        data = yf.download('GC=F', period="3mo", interval="1d", progress=False)
        if data.empty:
            return None
        return data
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {str(e)}")
        return None

data = get_gold_data()

if data is None or len(data) < 10:
    st.warning("البيانات غير متوفرة حاليًا أو غير كافية. جرب لاحقًا أو تحقق من الاتصال.")
else:
    # حساب المتوسطات
    data['EMA50']  = data['Close'].ewm(span=50,  adjust=False).mean()
    data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

    # استخراج القيم كـ scalars نقية باستخدام .item()
    current_price = data['Close'].iloc[-1].item()
    ema50         = data['EMA50'].iloc[-1].item()
    ema200        = data['EMA200'].iloc[-1].item()

    # الآن التحقق آمن 100% لأنها floats أو np.nan
    if np.isnan(current_price) or np.isnan(ema50) or np.isnan(ema200):
        bias  = "البيانات غير كافية (قيم مفقودة)"
        color = "gray"
    else:
        if (current_price > ema50) and (ema50 > ema200):
            bias = "صاعد قوي (Bullish Strong)"
            color = "green"
        elif current_price > ema50:
            bias = "صاعد (Bullish)"
            color = "lime"
        elif (current_price < ema50) and (ema50 < ema200):
            bias = "هابط قوي (Bearish Strong)"
            color = "red"
        else:
            bias = "جانبي / غير واضح (Range)"
            color = "orange"

    # دعم ومقاومة
    recent = data.tail(10)
    support    = recent['Low'].min().item()
    resistance = recent['High'].max().item()

    # عرض النتائج
    st.subheader("النتيجة الحالية:")
    st.metric("سعر الذهب الحالي", f"{current_price:,.2f} $")

    st.markdown(
        f"**الاتجاه**: <span style='color:{color}; font-weight:bold; font-size:1.4em;'>{bias}</span>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    col1.metric("EMA 50",  f"{ema50:,.2f}")
    col2.metric("EMA 200", f"{ema200:,.2f}")

    col3, col4 = st.columns(2)
    col3.metric("دعم قريب",    f"{support:,.2f}")
    col4.metric("مقاومة قريبة", f"{resistance:,.2f}")

    if len(data) < 200:
        st.info("ملاحظة: عدد الأيام أقل من 200، لذا قد لا تكون EMA 200 دقيقة جدًا.")

st.markdown("---")
st.caption("Powered by yfinance • يُحدّث كل ~15 دقيقة • تابع @fintech.cyberpunk على TikTok للمزيد")
