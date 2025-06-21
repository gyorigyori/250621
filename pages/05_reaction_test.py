import streamlit as st
import time
import random

st.set_page_config(page_title="반응속도 테스트", layout="centered")
st.title("⚡ 반응속도 테스트")

# 세션 상태 초기화
if "status" not in st.session_state:
    st.session_state.status = "ready"  # ready, waiting, clickable, done
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None

# 초기화 함수
def reset():
    st.session_state.status = "ready"
    st.session_state.start_time = None
    st.session_state.reaction_time = None

# 클릭 핸들링
def handle_click():
    if st.session_state.status == "clickable":
        rt = time.time() - st.session_state.start_time
        st.session_state.reaction_time = rt
        st.session_state.status = "done"

# 테스트 시작
def start_test():
    st.session_state.status = "waiting"
    delay = random.uniform(2, 5)
    time.sleep(delay)
    st.session_state.status = "clickable"
    st.session_state.start_time = time.time()

# 시작 버튼
if st.session_state.status == "ready":
    if st.button("테스트 시작"):
        start_test()

# 박스와 텍스트 출력
box_label = ""
box_color = "gray"

if st.session_state.status == "waiting":
    box_label = "wait"
    box_color = "red"

elif st.session_state.status == "clickable":
    box_label = "click"
    box_color = "green"

elif st.session_state.status == "done":
    box_label = f"{st.session_state.reaction_time:.3f} 초"
    box_color = "blue"

# 상자 UI
box_html = f"""
<div onclick="fetch('/_stcore/handle_click')" 
     style='width: 300px; height: 200px; background-color: {box_color}; 
     display: flex; align-items: center; justify-content: center; 
     font-size: 30px; font-weight: bold; color: white; cursor: pointer; 
     border-radius: 15px; margin: 30px auto;'>
    {box_label}
</div>
"""

# 클릭 핸들링 (클릭 시 실제 Python 처리)
clicked = st.button("여기를 클릭", on_click=handle_click, disabled=st.session_state.status != "clickable")

st.markdown(box_html, unsafe_allow_html=True)

# 다시하기 버튼
if st.session_state.status == "done":
    if st.button("🔁 다시하기"):
        reset()
