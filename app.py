
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="AI 주식 타이밍 알리미", layout="wide")

st.title("📈 AI 주식 타이밍 알리미")

st.sidebar.header("설정")

stock_name = st.sidebar.text_input("종목명", "삼성전자")

stock_map = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS",
    "LG에너지솔루션": "373220.KS",
}

ticker = stock_map.get(stock_name, "005930.KS")

short_ma = st.sidebar.slider("단기 이동평균", 3, 30, 5)
long_ma = st.sidebar.slider("장기 이동평균", 10, 120, 20)

st.sidebar.info("예시:\n005930.KS = 삼성전자\n000660.KS = SK하이닉스")

@st.cache_data
def load_data(ticker):
    ticker=ticker.strip().upper()

    data = yf.download(
        ticker,
        period="1y",
        interval="1d",
        progress=False,
        auto_adjust=False,
        )
    return data

df = load_data(ticker)

if df.empty:
    st.error("데이터를 불러오지 못했습니다.")
    st.stop()

df["Short_MA"] = df["Close"].rolling(short_ma).mean()
df["Long_MA"] = df["Close"].rolling(long_ma).mean()

delta = df["Close"].diff()
st.write(df.columns)
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
df["RSI"] = 100 - (100 / (1 + rs))

latest = df.iloc[-1]

buy_score = 0
sell_score = 0
reasons = []

if latest["Short_MA"].item()>latest["Long_MA"].item():
    buy_score += 30
    reasons.append("단기 이동평균 상승")

if latest["RSI"] .item()< 35:
    buy_score += 30
    reasons.append("RSI 과매도 구간")

if latest["RSI"] .item()> 70:
    sell_score += 40
    reasons.append("RSI 과열 구간")

recent_volume = df["Volume"].tail(5).mean()

if latest["Volume"] .item()> recent_volume.item() * 1.5:
    buy_score += 20
    reasons.append("거래량 증가")

if latest["Close"] .item()< latest["Short_MA"].item():
    sell_score += 30
    reasons.append("단기선 이탈")

st.subheader(f"📊 {ticker} 분석")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("현재가", f"{latest['Close'].item():.0f}")

with col2:
    st.metric("매수 점수", f"{buy_score}/100")

with col3:
    st.metric("매도 위험", f"{sell_score}/100")

if buy_score >= 50:
    st.success("🔵 상승 가능성 관심 구간")

if sell_score >= 50:
    st.error("🔴 하락 위험 주의")

st.write("### AI 분석 이유")
for r in reasons:
    st.write(f"- {r}")

st.write("### 최근 데이터")
st.dataframe(df.tail(10))

st.info("""
⚠️ 이 앱은 투자 참고용입니다.
100% 정확한 예측은 불가능하며 투자 책임은 본인에게 있습니다.
""")
