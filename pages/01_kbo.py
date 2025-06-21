import streamlit as st
import pandas as pd
import urllib.request

# 🛡️ 사용자 브라우저처럼 보이도록 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

date = "2025-06-19"
url = f"http://www.statiz.co.kr/boxscore.php?date={date}"

st.title("📅 2025년 6월 19일 KBO 경기 결과 (Statiz 크롤링)")

try:
    # ✅ User-Agent 포함한 요청 생성
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    # ✅ HTML을 pandas로 파싱
    tables = pd.read_html(html)
    result_list = []

    for table in tables:
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
                continue

    if result_list:
        st.success(f"✅ {date} 경기 결과:")
        for team, result in result_list:
            st.markdown(f"- **{team}**: {result}")
    else:
        st.warning("❗경기 결과가 없거나 경기가 진행되지 않았습니다.")

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")
