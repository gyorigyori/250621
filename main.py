import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 🎨 팀별 색상
TEAM_COLORS = {
    "LG": "#860038", "KT": "#000000", "SSG": "#E60012", "NC": "#1C1C1C",
    "KIA": "#EF3E42", "롯데": "#0E3386", "두산": "#13274F", "삼성": "#005BAC",
    "한화": "#FA4616", "키움": "#6F2DA8"
}

# 📡 KBO 경기 결과 크롤링 함수 (스탯티즈 기준)
def fetch_results(start_date, end_date):
    result_data = []

    base_url = "https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}"
    date_list = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d')

    for game_date in date_list:
        url = base_url.format(date=game_date)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        games = soup.select("div.scheduleList ul li")

        for game in games:
            try:
                teams = game.select("span.team")
                scores = game.select("span.score")

                if len(teams) < 2 or len(scores) < 2:
                    continue

                team1 = teams[0].text.strip()
                team2 = teams[1].text.strip()
                score1 = int(scores[0].text.strip())
                score2 = int(scores[1].text.strip())

                # 승패 판단
                if score1 > score2:
                    result_data.append({"date": game_date, "team": team1, "result": "win"})
                    result_data.append({"date": game_date, "team": team2, "result": "lose"})
                elif score1 < score2:
                    result_data.append({"date": game_date, "team": team1, "result": "lose"})
                    result_data.append({"date": game_date, "team": team2, "result": "win"})
                else:
                    result_data.append({"date": game_date, "team": team1, "result": "draw"})
                    result_data.append({"date": game_date, "team": team2, "result": "draw"})

            except Exception as e:
                continue  # skip parsing error

    return pd.DataFrame(result_data)

# 📊 승패마진 계산 함수
def calculate_win_margin(df):
    df['win'] = df['result'].apply(lambda x: 1 if x == 'win' else 0)
    df['loss'] = df['result'].apply(lambda x: 1 if x == 'lose' else 0)
    df['margin'] = df['win'] - df['loss']
    df_grouped = df.groupby(['team', 'date'])['margin'].sum().reset_index()
    df_grouped['cumulative'] = df_grouped.groupby('team')['margin'].cumsum()
    return df_grouped

# 🖥️ Streamlit 인터페이스
st.set_page_config(page_title="KBO 승패마진 자동크롤링", layout="wide")
st.title("⚾ KBO 리그 팀별 날짜별 승패마진 추적기")
st.markdown("실시간으로 경기 결과를 크롤링하고 그래프를 그려줍니다.")

# 날짜 입력
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 시작 날짜", datetime.today() - timedelta(days=7))
with col2:
    end_date = st.date_input("📅 종료 날짜", datetime.today())

if start_date > end_date:
    st.error("시작 날짜는 종료 날짜보다 앞서야 합니다.")
else:
    if st.button("🔍 결과 가져오기 및 그래프 그리기"):
        with st.spinner("KBO 경기 결과 크롤링 중..."):
            result_df = fetch_results(start_date, end_date)

            if result_df.empty:
                st.warning("해당 기간에 경기 결과가 없습니다.")
            else:
                margin_df = calculate_win_margin(result_df)

                # 📈 그래프 그리기
                st.subheader("📈 팀별 누적 승패마진 그래프")
                fig, ax = plt.subplots(figsize=(12, 6))

                for team in margin_df['team'].unique():
                    team_data = margin_df[margin_df['team'] == team]
                    ax.plot(team_data['date'], team_data['cumulative'],
                            label=team, color=TEAM_COLORS.get(team, None), linewidth=2)

                ax.set_xlabel("날짜")
                ax.set_ylabel("승패마진")
                ax.set_title("날짜별 승패마진 누적 변화")
                ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
                ax.grid(True)

                st.pyplot(fig)

                # 원본 데이터 보기
                with st.expander("📄 원본 데이터 보기"):
                    st.dataframe(result_df)
