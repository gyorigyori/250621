import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 🎨 팀 색상
TEAM_COLORS = {
    "LG": "#860038", "KT": "#000000", "SSG": "#E60012", "NC": "#1C1C1C",
    "KIA": "#EF3E42", "롯데": "#0E3386", "두산": "#13274F", "삼성": "#005BAC",
    "한화": "#FA4616", "키움": "#6F2DA8"
}

# ⚾ Statiz 크롤링 함수
def fetch_statiz_results(start_date, end_date):
    all_results = []
    date_range = pd.date_range(start=start_date, end=end_date)

    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        url = f"http://www.statiz.co.kr/boxscore.php?date={date_str}"

        try:
            tables = pd.read_html(url)
            for table in tables:
                if table.shape[1] >= 5 and '팀' in table.columns[0]:
                    # 각 경기의 승/패 판단
                    team1 = table.iloc[0, 0]
                    team2 = table.iloc[1, 0]
                    score1 = int(table.iloc[0, 1])
                    score2 = int(table.iloc[1, 1])

                    if score1 > score2:
                        all_results.append({"date": date_str, "team": team1, "result": "win"})
                        all_results.append({"date": date_str, "team": team2, "result": "lose"})
                    elif score1 < score2:
                        all_results.append({"date": date_str, "team": team1, "result": "lose"})
                        all_results.append({"date": date_str, "team": team2, "result": "win"})
                    else:
                        all_results.append({"date": date_str, "team": team1, "result": "draw"})
                        all_results.append({"date": date_str, "team": team2, "result": "draw"})
        except Exception:
            continue  # 날짜에 경기 없거나 파싱 실패 시 넘어감

    return pd.DataFrame(all_results)

# 📊 승패마진 계산 함수
def calculate_margin(df):
    df['win'] = df['result'].apply(lambda x: 1 if x == 'win' else 0)
    df['loss'] = df['result'].apply(lambda x: 1 if x == 'lose' else 0)
    df['margin'] = df['win'] - df['loss']
    grouped = df.groupby(['team', 'date'])['margin'].sum().reset_index()
    grouped['cumulative'] = grouped.groupby('team')['margin'].cumsum()
    return grouped

# 🖥️ Streamlit UI
st.set_page_config(page_title="Statiz 기반 KBO 승패마진", layout="wide")
st.title("📊 KBO 팀별 승패마진 추적기 (Statiz 기반)")
st.markdown("날짜 범위를 설정하면 Statiz에서 경기 결과를 가져와 승패마진을 시각화합니다.")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 시작 날짜", datetime.today() - timedelta(days=7))
with col2:
    end_date = st.date_input("📅 종료 날짜", datetime.today())

if start_date > end_date:
    st.error("❌ 시작 날짜는 종료 날짜보다 앞서야 합니다.")
elif st.button("📡 경기 결과 가져오기"):
    with st.spinner("Statiz에서 경기 결과 크롤링 중..."):
        df = fetch_statiz_results(start_date, end_date)

    if df.empty:
        st.warning("해당 날짜 범위에 경기 정보가 없습니다.")
    else:
        margin_df = calculate_margin(df)

        st.subheader("📈 팀별 누적 승패마진 그래프")
        fig, ax = plt.subplots(figsize=(12, 6))

        for team in margin_df['team'].unique():
            team_data = margin_df[margin_df['team'] == team]
            ax.plot(team_data['date'], team_data['cumulative'],
                    label=team, color=TEAM_COLORS.get(team, None), linewidth=2)

        ax.set_xlabel("날짜")
        ax.set_ylabel("누적 승패마진")
        ax.set_title("KBO 팀별 누적 승패마진")
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(True)
        st.pyplot(fig)

        with st.expander("🔍 크롤링된 원본 데이터 보기"):
            st.dataframe(df)
