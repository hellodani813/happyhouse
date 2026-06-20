import streamlit as st
from datetime import datetime, date

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="창준 & 다영의 스케쥴러",
    page_icon="🏡",
    layout="centered"
)

# 모바일 화면 전용 커스텀 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=300;400;500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FAF6F0; /* 포근한 크림색 */
    }
    
    .stButton>button {
        width: 100%;
        background-color: #E6A15C; 
        color: white;
        border-radius: 12px;
        padding: 10px;
        font-size: 16px;
        border: none;
        font-weight: bold;
    }
    
    .schedule-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03);
        border: 1px solid #F1EFEA;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .card-date {
        font-size: 14px;
        color: #8C8A85;
        font-weight: 500;
    }
    
    .card-content {
        font-size: 16px;
        color: #333333;
        font-weight: 500;
        line-height: 1.4;
    }
    
    .user-tag {
        padding: 3px 8px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
    }
    .cj-tag { background-color: #E6F4FF; color: #0958D9; }
    .dy-tag { background-color: #FFF7E6; color: #D46B08; }
    .together-tag { background-color: #F6FFED; color: #389E0D; }
    </style>
""", unsafe_allow_html=True)

# 2. 가상 데이터베이스 초기화 (예시 데이터 무드 변경)
if 'events' not in st.session_state:
    st.session_state.events = [
        {"date": date(2026, 6, 21), "user": "이창준", "content": "주말 마트 장보기", "mood": "🍱 식사/장보기"},
        {"date": date(2026, 6, 23), "user": "이다영", "content": "중요한 프로젝트 마감", "mood": "💼 회사/출근"},
        {"date": date(2026, 6, 25), "user": "함께", "content": "영화 보러 가기!", "mood": "🎉 놀기/휴식"}
    ]

# 3. 모바일 상단 헤더
st.markdown("<h3 style='margin-bottom:0px; font-size:20px;'>🏡 우리들의 아지트</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='margin-top:0px; font-size:28px;'>창준 🤎 다영</h1>", unsafe_allow_html=True)

# 4. 일정 추가하기
with st.expander("✨ 새로운 일정 적기", expanded=False):
    event_date = st.date_input("날짜 선택", date.today())
    event_user = st.selectbox("누구의 일정?", ["이창준", "이다영", "함께"])
    
    # 🌟 요청하신 무드 카테고리 적용 부분!
    event_mood = st.selectbox(
        "오늘의 무드는?", 
        [
            "💼 회사/출근", 
            "🏫 학교/등교", 
            "🍱 식사/장보기", 
            "📝 공부/자기계발", 
            "🎉 놀기/휴식", 
            "🕊️ 개인용무", 
            "💡 기타"
        ]
    )
    
    event_content = st.text_input("무엇을 하나요?", placeholder="예: 맛있는 맛집 가기")
    
    st.write("") 
    if st.button("우리 공간에 저장하기 📝"):
        if event_content:
            st.session_state.events.append({
                "date": event_date,
                "user": event_user,
                "content": event_content,
                "mood": event_mood
            })
            st.session_state.events = sorted(st.session_state.events, key=lambda x: x['date'])
            st.toast("일정이 예쁘게 등록되었어요! 🕊️")
            st.rerun()
        else:
            st.warning("내용을 입력해주세요!")

st.markdown("---")

# 5. 모바일 타임라인
st.markdown("<h4 style='font-size:18px; margin-bottom:15px;'>🗓️ 다가오는 일정</h4>", unsafe_allow_html=True)

if not st.session_state.events:
    st.info("비어있어요. 우리들만의 이야기를 채워주세요 🧸")
else:
    for idx, ev in enumerate(st.session_state.events):
        if ev['user'] == "이창준":
            tag_html = '<span class="user-tag cj-tag">창준🙋‍♂️</span>'
        elif ev['user'] == "이다영":
            tag_html = '<span class="user-tag dy-tag">다영🙋‍♀️</span>'
        else:
            tag_html = '<span class="user-tag together-tag">함께💕</span>'
            
        date_str = ev['date'].strftime("%m월 %d일 (%a)")
        
        # HTML 카드 내에 선택한 무드가 이모지와 함께 노출됩니다.
        st.markdown(f"""
            <div class="schedule-card">
                <div class="card-header">
                    <span class="card-date">📅 {date_str}</span>
                    {tag_html}
                </div>
                <div class="card-content">
                    <small style='color:#A8A6A1; font-weight:normal;'>[{ev['mood']}]</small><br>
                    {ev['content']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_space, col_del = st.columns([6, 1])
        with col_del:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.events.pop(idx)
                st.rerun()

# 6. 하단 푸터
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<center style='opacity: 0.5; font-size: 12px;'>Changjun & Dayoung Space 🤎</center>", unsafe_allow_html=True)
