import streamlit as st
import time
import random

st.set_page_config(page_title="반응속도 테스트", page_icon="⚡", layout="centered")

st.title("⚡ 반응속도 테스트")
st.write("아래 버튼을 눌러 시작하세요. 화면이 바뀌면 가능한 빨리 클릭하세요!")

# 세션 상태 초기화
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "reaction_times" not in st.session_state:
    st.session_state.reaction_times = []
if "waiting" not in st.session_state:
    st.session_state.waiting = False

def start_test():
    st.session_state.waiting = True
    st.session_state.start_time = None
    delay = random.uniform(2, 5)  # 2초에서 5초 사이 무작위 대기
    time.sleep(delay)
    st.session_state.start_time = time.time()
    st.session_state.waiting = False

if st.button("테스트 시작", disabled=st.session_state.waiting):
    start_test()

# 반응 버튼 표시
if st.session_state.start_time:
    clicked = st.button("지금 클릭하세요!", type="primary")
    if clicked:
        reaction_time = time.time() - st.session_state.start_time
        st.session_state.reaction_times.append(reaction_time)
        st.session_state.start_time = None
        st.success(f"⏱ 반응속도: {reaction_time:.3f} 초")

# 결과 표시
if st.session_state.reaction_times:
    st.subheader("📊 결과")
    st.write(f"총 시도 횟수: {len(st.session_state.reaction_times)}")
    st.write(f"평균 반응속도: {sum(st.session_state.reaction_times) / len(st.session_state.reaction_times):.3f} 초")
    st.line_chart(st.session_state.reaction_times)

# 리셋 기능
if st.button("결과 초기화"):
    st.session_state.reaction_times = []
    st.session_state.start_time = None
    st.session_state.waiting = False
    st.experimental_rerun()
