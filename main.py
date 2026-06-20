import streamlit as pd
import streamlit as st
from datetime import datetime, date

# 1. 페이지 기본 설정 및 감성 테마 (Cozy Warm)
st.set_page_config(
    page_title="창준 & 다영의 스케쥴러",
    page_icon="🏡",
    layout="centered"
)

# 커스텀 CSS로 트렌디하고 포근한 느낌 주기
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FAF6F0; /* 따뜻한 크림색 배경 */
    }
    .stButton>button {
        background-color: #E6A15C; /* 따뜻한 귤색 */
        color: white;
        border-radius: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #CD853F;
        color: white;
    }
    .user-badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
    }
    .cj-badge { background-color: #D6E4FF; color: #1D39C4; } /* 창준: 포근한 블루 */
    .dy-badge { background-color: #FFE7BA; color: #D46B08; } /* 다영: 따뜻한 오렌지 */
    .together-badge { background-color: #F6FFED; color: #389E0D; } /* 함께: 싱그러운 그린 */
    </style>
""", unsafe_allow_html=True)

# 2. 가상 데이터베이스 초기화 (스트림릿 세션 상태 사용)
if 'events' not in st.session_state:
    st.session_state.events = [
        {"date": date(2026, 6, 21), "user": "이창준", "content": "🛒 주말 마트 장보기", "emoji": "📦"},
        {"date": date(2026, 6, 23), "user": "이다영", "content": "💇‍♀️ 미용실 예약 (퇴근 후)", "emoji": "✨"},
        {"date": date(2026, 6, 25), "user": "함께", "content": "🎬 영화 보면서 맛있는 거 먹기!", "emoji": "🍿"}
    ]

# 3. 헤더 영역
st.write("### 🏡 우리들의 소소한 기록")
st.title("창준 🤎 다영 스케줄러")
st.write("오늘도 서로의 하루를 응원해요. ✨")
st.markdown("---")

# 4. 일정 추가하기 (사이드바 또는 상단 접이식 메뉴)
with st.expander("🎈 새로운 일정 추가하기", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("언제인가요?", date.today())
        event_user = st.selectbox("누구의 일정인가요?", ["이창준", "이다영", "함께"])
    with col2:
        event_emoji = st.selectbox("오늘의 무드 이모지", ["🥰", "📅", "🍰", "🛒", "🍿", "💪", "✈️", "💼"])
        event_content = st.text_input("무엇을 하나요?", placeholder="예: 맛있는 저녁 먹기")
    
    if st.button("우리 집에 일정 등록하기 🏠"):
        if event_content:
            st.session_state.events.append({
                "date": event_date,
                "user": event_user,
                "content": event_content,
                "emoji": event_emoji
            })
            # 날짜 정렬
            st.session_state.events = sorted(st.session_state.events, key=lambda x: x['date'])
            st.toast("새로운 일정이 포근하게 저장되었어요! 📝")
            st.rerun()
        else:
            st.warning("일정 내용을 입력해주세요!")

# 5. 일정 타임라인 보여주기
st.write("#### 🗓️ 다가오는 일정 목록")

if not st.session_state.events:
    st.info("아직 등록된 일정이 없어요. 새로운 추억을 채워주세요!")
else:
    # 날짜별로 그룹화하여 예쁘게 출력
    for idx, ev in enumerate(st.session_state.events):
        # 유저별 배지 지정
        if ev['user'] == "이창준":
            badge = f'<span class="user-badge cj-badge">🙋‍♂️ 창준</span>'
        elif ev['user'] == "이다영":
            badge = f'<span class="user-badge dy-badge">🙋‍♀️ 다영</span>'
        else:
            badge = f'<span class="user-badge together-badge">💕 함께</span>'
            
        # 가독성 좋은 날짜 포맷
        date_str = ev['date'].strftime("%m월 %d일 (%a)")
        
        # 일정 한 줄 레이아웃
        col_date, col_content, col_del = st.columns([2, 5, 1])
        
        with col_date:
            st.write(f"**{date_str}**")
        with col_content:
            st.markdown(f"{ev['emoji']} {ev['content']}  {badge}", unsafe_allow_html=True)
        with col_del:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.events.pop(idx)
                st.rerun()
        
        st.markdown("<hr style='margin: 8px 0; border-top: 1px dashed #ddd;'>", unsafe_allow_html=True)

# 6. 감성 하단 레이아웃
st.markdown("---")
st.caption("Designed with 🤎 for Changjun & Dayoung")
