import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="반응속도 테스트", layout="centered")

st.title("⚡ 반응속도 테스트")
st.markdown("닉네임을 입력하고 테스트를 시작하세요!")

# 사용자 닉네임 입력
nickname = st.text_input("닉네임", max_chars=20)

# 세션 상태 초기화
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None
if "test_ready" not in st.session_state:
    st.session_state.test_ready = False
if "can_click" not in st.session_state:
    st.session_state.can_click = False
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# 테스트 시작 로직
def start_test():
    st.session_state.reaction_time = None
    st.session_state.test_ready = True
    st.session_state.can_click = False
    delay = random.uniform(2, 5)

    placeholder = st.empty()
    placeholder.markdown('<div style="height:300px; background-color:red;"></div>', unsafe_allow_html=True)
    time.sleep(delay)

    st.session_state.start_time = time.time()
    st.session_state.can_click = True
    placeholder.markdown('<div style="height:300px; background-color:green;"></div>', unsafe_allow_html=True)
    
    if st.button("지금 클릭!"):
        register_reaction()

# 반응 기록
def register_reaction():
    if st.session_state.can_click and st.session_state.start_time:
        rt = time.time() - st.session_state.start_time
        st.session_state.reaction_time = rt
        st.success(f"⏱ 반응속도: {rt:.3f} 초")
        st.session_state.can_click = False

        # 리더보드에 기록 추가
        st.session_state.leaderboard.append({"닉네임": nickname, "반응속도": rt})
    else:
        st.warning("아직 초록 화면이 아닙니다!")

# 닉네임 없으면 테스트 비활성화
if nickname.strip() == "":
    st.warning("닉네임을 입력하세요.")
else:
    if st.button("테스트 시작", disabled=st.session_state.test_ready):
        start_test()

# 리더보드 표시
if st.session_state.leaderboard:
    st.subheader("🏆 리더보드 (빠른 순)")
    df = pd.DataFrame(st.session_state.leaderboard)
    df = df.sort_values("반응속도").reset_index(drop=True)
    st.dataframe(df.style.highlight_min("반응속도", color="lightgreen"), use_container_width=True)

# 초기화 버튼
if st.button("리더보드 초기화"):
    st.session_state.leaderboard = []
    st.success("리더보드를 초기화했습니다.")
