import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("📈 글로벌 시가총액 Top 10 기업 - 최근 1년 주가 변화 시각화")

# 글로벌 시가총액 Top 10 기업 (2025년 기준 가정)
tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'NVIDIA': 'NVDA',
    'Meta (Facebook)': 'META',
    'Berkshire Hathaway': 'BRK-B',
    'TSMC': 'TSM',
    'Eli Lilly': 'LLY'
}

start_date = datetime.today() - timedelta(days=365)
end_date = datetime.today()

# 데이터를 가져옴
st.write("⏳ 데이터를 불러오는 중...")
data = {}
for name, symbol in tickers.items():
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start=start_date, end=end_date)
    data[name] = hist['Close']

# 데이터프레임으로 변환
df = pd.DataFrame(data)
df.index = df.index.date  # 날짜 포맷 간결화

# Plotly 시각화
fig = go.Figure()
for company in df.columns:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[company],
        mode='lines',
        name=company
    ))

fig.update_layout(
    title="글로벌 시가총액 TOP 10 기업 주가 변화 (최근 1년)",
    xaxis_title="날짜",
    yaxis_title="종가 (USD)",
    hovermode='x unified',
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
