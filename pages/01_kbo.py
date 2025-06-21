import streamlit as st
import pandas as pd

# Streamlit 앱 제목
st.title("📅 2025년 6월 19일 KBO 경기 결과 (Statiz 크롤링)")

# 대상 날짜
date = "2025-06-19"
url = f"http://www.statiz.co.kr/boxscore.php?date={date}"

# 크롤링 및 결과 처리
try:
    tables = pd.read_html(url)
    result_list = []

    for table in tables:
        # 팀명 테이블만 필터링
        if table.shape[0] >= 2 and '팀' in table.columns[0]:
            try:
                team1 = table.iloc[0, 0]
                team2 = table.iloc[1, 0]
                score1 = int(table.iloc[0, 1])
                score2 = int(table.iloc[1, 1])

                if score1 > score2:
                    result_list.append((team1, "승리 🏆"))
                    result_list.append((team2, "패배 ❌"))
                elif score1 < score2:
                    result_list.append((team1, "패배 ❌"))
                    result_list.append((team2, "승리 🏆"))
                else:
                    result_list.append((team1, "무승부 🤝"))
                    result_list.append((team2, "무승부 🤝"))

            except ValueError:
                # 점수가 '-' 인 경우 (경기 전) 무시
                continue

    if result_list:
        st.success(f"✅ {date} 경기 결과:")
        for team, result in result_list:
            st.markdown(f"- **{team}**: {result}")
    else:
        st.warning("❗해당 날짜에 경기 결과가 없거나 경기가 진행되지 않았습니다.")

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")
