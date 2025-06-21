import streamlit as st
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(page_title="방학 디데이 타이머", layout="centered")
st.title("🎉 방학까지 D-Day 타이머")

# D-Day 설정
d_day = datetime(2025, 7, 21, 10, 0, 0)

# 타이머 표시 공간
timer_placeholder = st.empty()

# 타이머 루프
while True:
    now = datetime.now()
    remaining = d_day - now

    if remaining.total_seconds() <= 0:
        timer_placeholder.markdown("🎊 **드디어 방학입니다! 즐거운 시간 보내세요!** 🎊")
        break

    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(remaining.microseconds / 1000)

    # 한 줄 출력
    countdown_str = f"⏳ 남은 시간: {days:02d}일 {hours:02d}시간 {minutes:02d}분 {seconds:02d}초 {milliseconds:03d}ms"
    timer_placeholder.markdown(f"<h2 style='text-align: center;'>{countdown_str}</h2>", unsafe_allow_html=True)

    time.sleep(0.05)  # 약 20fps 정도의 업데이트 속도
