import streamlit as st
from datetime import date
import calendar

st.set_page_config(
    page_title="우리의 가족 캘린더",
    page_icon="🏡",
    layout="wide"
)

# --------------------
# 스타일
# --------------------
st.markdown("""
<style>
.main {
    background-color: #f8f5f0;
}

.title-box {
    text-align:center;
    padding:20px;
    border-radius:20px;
    background:#fffaf3;
    border:1px solid #ebe3d6;
    margin-bottom:20px;
}

.day-card {
    background:white;
    border:1px solid #e9e1d5;
    border-radius:12px;
    padding:8px;
    min-height:140px;
}

.schedule-item {
    background:#f5eee3;
    padding:4px 8px;
    border-radius:8px;
    margin-bottom:4px;
    font-size:13px;
}

.member-husband {
    color:#4a6fa5;
    font-weight:bold;
}

.member-wife {
    color:#c76d7e;
    font-weight:bold;
}

.week-header {
    text-align:center;
    font-weight:bold;
    color:#6b6257;
    padding:8px;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# 데이터 저장
# --------------------
if "events" not in st.session_state:
    st.session_state.events = {}

# --------------------
# 헤더
# --------------------
st.markdown("""
<div class="title-box">
    <h1>🏡 우리의 가족 캘린더</h1>
    <p>신랑과 신부의 일정을 함께 관리해요</p>
</div>
""", unsafe_allow_html=True)

# --------------------
# 일정 등록
# --------------------
with st.expander("➕ 일정 추가", expanded=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_date = st.date_input(
            "날짜",
            value=date.today()
        )

    with col2:
        member = st.selectbox(
            "가족 구성원",
            ["🤵 신랑", "👰 신부"]
        )

    with col3:
        title = st.text_input("일정")

    if st.button("일정 저장", use_container_width=True):
        if title.strip():

            key = str(selected_date)

            if key not in st.session_state.events:
                st.session_state.events[key] = []

            st.session_state.events[key].append({
                "member": member,
                "title": title
            })

            st.success("일정이 저장되었습니다.")

# --------------------
# 월 선택
# --------------------
today = date.today()

col1, col2 = st.columns(2)

with col1:
    year = st.selectbox(
        "연도",
        list(range(today.year - 3, today.year + 4)),
        index=3
    )

with col2:
    month = st.selectbox(
        "월",
        list(range(1, 13)),
        index=today.month - 1
    )

# --------------------
# 달력 생성
# --------------------
st.markdown("### 📅 월간 일정")

week_names = ["월", "화", "수", "목", "금", "토", "일"]

cols = st.columns(7)
for col, day_name in zip(cols, week_names):
    col.markdown(
        f"<div class='week-header'>{day_name}</div>",
        unsafe_allow_html=True
    )

cal = calendar.Calendar(firstweekday=0)
month_days = cal.monthdayscalendar(year, month)

for week in month_days:

    cols = st.columns(7)

    for idx, day_num in enumerate(week):

        with cols[idx]:

            if day_num == 0:
                st.write("")
                continue

            current_date = date(year, month, day_num)
            key = str(current_date)

            html = f"""
            <div class='day-card'>
                <strong>{day_num}</strong><br><br>
            """

            if key in st.session_state.events:

                for event in st.session_state.events[key]:

                    cls = (
                        "member-husband"
                        if event["member"] == "🤵 신랑"
                        else "member-wife"
                    )

                    html += f"""
                    <div class='schedule-item'>
                        <span class='{cls}'>
                            {event["member"]}
                        </span><br>
                        {event["title"]}
                    </div>
                    """

            html += "</div>"

st.container(border=True)

st.markdown(f"**{day_num}**")

if key in st.session_state.events:
    for event in st.session_state.events[key]:

        if event["member"] == "🤵 신랑":
            st.info(f"{event['member']} {event['title']}")
        else:
            st.warning(f"{event['member']} {event['title']}")

# --------------------
# 일정 목록 및 삭제
# --------------------
st.markdown("---")
st.markdown("### 📝 전체 일정")

all_events = []

for d, items in st.session_state.events.items():
    for i, event in enumerate(items):
        all_events.append((d, i, event))

if not all_events:
    st.info("등록된 일정이 없습니다.")
else:

    all_events.sort(key=lambda x: x[0])

    for d, idx, event in all_events:

        c1, c2 = st.columns([6, 1])

        with c1:
            st.write(
                f"**{d}** | {event['member']} | {event['title']}"
            )

        with c2:
            if st.button(
                "삭제",
                key=f"{d}_{idx}"
            ):
                st.session_state.events[d].pop(idx)

                if not st.session_state.events[d]:
                    del st.session_state.events[d]

                st.rerun()
