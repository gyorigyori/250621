import streamlit as st

# 🧠 MBTI와 직업 매핑
mbti_jobs = {
    "INTJ": ["🔬 과학자", "📊 데이터 분석가", "💻 소프트웨어 엔지니어"],
    "INFP": ["🎨 작가", "🎭 예술가", "🧘‍♀️ 상담사"],
    "ENTP": ["💡 스타트업 창업가", "🎤 마케팅 전문가", "📺 방송인"],
    "ESFJ": ["🧑‍🏫 교사", "👩‍⚕️ 간호사", "🎉 이벤트 플래너"],
    "ISTJ": ["👨‍💼 회계사", "🧑‍✈️ 군인", "🏦 은행원"],
    "ENFP": ["🎬 영화감독", "🎨 디자이너", "🌍 여행 가이드"],
    "ISFP": ["🎻 음악가", "📸 사진작가", "🌿 플로리스트"],
    "ESTP": ["🚓 경찰", "📣 세일즈", "💪 퍼스널 트레이너"],
    # 나머지 유형도 추가 가능
}

# 🌟 Streamlit 앱 구성
st.set_page_config(page_title="MBTI 직업 추천기", page_icon="🌈", layout="wide")

st.markdown(
    """
    <div style="text-align:center">
        <h1 style="color:#FF69B4">🌈 MBTI 기반 진로 추천 앱 💼</h1>
        <h3>✨ 당신의 성격 유형에 맞는 직업을 찾아드릴게요! ✨</h3>
        <p style="font-size:24px;">이모지와 함께 화려한 추천을 받아보세요 🎉</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 🎯 MBTI 선택
selected_mbti = st.selectbox("👇 당신의 MBTI를 선택해주세요", list(mbti_jobs.keys()))

st.markdown("---")

# 💼 직업 추천 출력
if selected_mbti:
    st.subheader(f"🎯 {selected_mbti} 유형에게 어울리는 직업은...")
    for job in mbti_jobs[selected_mbti]:
        st.markdown(f"### {job}")
    st.balloons()

# 🖼️ 배경 스타일 (CSS)
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
    }
    .stApp {
        background-image: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
        color: #000000;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
