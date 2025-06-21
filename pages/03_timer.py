import streamlit as st
from datetime import datetime, timedelta
import time

# 제목
st.title("🎉 방학까지 D-Day 타이머")

# D-Day 설정 (2025년 7월 21일 10시)
d_day = datetime(2025, 7, 21, 10, 0, 0)

# 타이머 반복 업데이트 (실시간 카운트다운)
placeholder = st.empty()

while True:
    now = datetime.now()
    remaining = d_day - now

    if remaining.total_seconds() <= 0:
        placeholder.markdown("🎊 **드디어 방학입니다! 즐거운 시간 보내세요!** 🎊")
        break

    # 남은 시간 계산
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # 출력
    with placeholder.container():
        st.subheader("⏳ 남은 시간:")
        st.metric("일", f"{days}")
        st.metric("시간", f"{hours}")
        st.metric("분", f"{minutes}")
        st.metric("초", f"{seconds}")

    time.sleep(1)
