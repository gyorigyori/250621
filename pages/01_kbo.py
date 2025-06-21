import streamlit as st
from pykbo import kbo

st.title("📅 KBO 경기 결과 (pykbo 라이브러리 사용)")
date = "2025-06-19"

try:
    kbo_obj = kbo.KBO()
    results = kbo_obj.get_game_info(date)

    if not results:
        st.warning("경기 정보가 없습니다.")
    else:
        for game in results:
            away = game["away_team"]
            home = game["home_team"]
            away_score = game["away_score"]
            home_score = game["home_score"]

            if away_score > home_score:
                winner = f"{away} 승리 🏆"
            elif home_score > away_score:
                winner = f"{home} 승리 🏆"
            else:
                winner = "무승부 🤝"

            st.markdown(f"**{away}** {away_score} : {home_score} **{home}** → {winner}")

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")
