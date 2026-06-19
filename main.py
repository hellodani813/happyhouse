
import streamlit as st
import calendar
import uuid
from datetime import date, datetime

# -----------------------------
# 기본 설정
# -----------------------------

st.set_page_config(
    page_title="우리 가족 캘린더",
    page_icon="🌷",
    layout="wide"
)

# -----------------------------
# 스타일
# -----------------------------

st.markdown("""
<style>

.stApp{
    background:linear-gradient(
        180deg,
        #fff9fb 0%,
        #f7fbff 100%
    );
}

.title{
    text-align:center;
    font-size:3rem;
    font-weight:800;
    color:#6c7cff;
}

.subtitle{
    text-align:center;
    color:#888;
    margin-bottom:20px;
}

.calendar-cell{
    background:white;
    border-radius:18px;
    min-height:150px;
    padding:8px;
    border:1px solid #ececec;
    box-shadow:0 3px 10px rgba(0,0,0,0.05);
}

.today{
    border:3px solid #ff9dc5;
}

.card{
    background:white;
    border-radius:18px;
    padding:20px;
    box-shadow:0 3px 10px rgba(0,0,0,0.05);
}

.schedule-item{
    border-radius:8px;
    padding:4px 6px;
    margin-top:4px;
    font-size:12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 데이터
# -----------------------------

if "schedules" not in st.session_state:
    st.session_state.schedules = []

# -----------------------------
# 색상
# -----------------------------

member_colors = {
    "💙 아빠": "#dff1ff",
    "💖 엄마": "#ffdff0",
    "🌟 첫째": "#fff4bf",
    "🍀 둘째": "#dcf8d5",
    "🎉 가족행사": "#ebe1ff"
}

# -----------------------------
# 헤더
# -----------------------------

st.markdown(
    "<div class='title'>🌷 우리 가족 캘린더 🌷</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>가족 모두의 일정을 한눈에 확인해보세요 👨‍👩‍👧‍👦</div>",
    unsafe_allow_html=True
)

# -----------------------------
# 달력 함수
# -----------------------------

def draw_calendar(year, month):

    st.markdown("### 📅 월간 캘린더")

    weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    cols = st.columns(7)

    for i, d in enumerate(weekdays):
        cols[i].markdown(
            f"<center><b>{d}</b></center>",
            unsafe_allow_html=True
        )

    cal = calendar.monthcalendar(year, month)

    today = date.today()

    for week in cal:

        cols = st.columns(7)

        for idx, day in enumerate(week):

            if day == 0:
                cols[idx].empty()
                continue

            day_events = []

            for s in st.session_state.schedules:

                dt = datetime.strptime(
                    s["date"],
                    "%Y-%m-%d"
                )

                if (
                    dt.year == year and
                    dt.month == month and
                    dt.day == day
                ):
                    day_events.append(s)

            today_class = ""

            if (
                today.year == year and
                today.month == month and
                today.day == day
            ):
                today_class = "today"

            html = f"""
            <div class='calendar-cell {today_class}'>
            <b>{day}</b>
            """

            for event in day_events[:4]:

                color = member_colors[event["member"]]

                html += f"""
                <div
                class='schedule-item'
                style='background:{color};'>
                {event["member"].split()[0]}
                {event["title"]}
                </div>
                """

            if len(day_events) > 4:
                html += f"<small>+{len(day_events)-4}개</small>"

            html += "</div>"

            cols[idx].markdown(
                html,
                unsafe_allow_html=True
            )

# -----------------------------
# 월 선택
# -----------------------------

today = date.today()

c1, c2 = st.columns([1,1])

with c1:
    year = st.selectbox(
        "📆 연도",
        list(range(2024, 2036)),
        index=today.year - 2024
    )

with c2:
    month = st.selectbox(
        "🗓️ 월",
        list(range(1,13)),
        index=today.month - 1
    )

draw_calendar(year, month)

st.divider()

# -----------------------------
# 일정 추가
# -----------------------------

left, right = st.columns([1,1])

with left:

    st.markdown("### ➕ 일정 추가")

    member = st.selectbox(
        "가족 구성원",
        [
            "💙 아빠",
            "💖 엄마",
            "🌟 첫째",
            "🍀 둘째",
            "🎉 가족행사"
        ]
    )

    schedule_date = st.date_input(
        "날짜",
        value=today
    )

    title = st.text_input(
        "일정 제목",
        placeholder="예: 치과 방문"
    )

    time = st.text_input(
        "시간",
        placeholder="예: 14:00"
    )

    if st.button("🌸 일정 저장", use_container_width=True):

        if title:

            st.session_state.schedules.append({
                "id": str(uuid.uuid4()),
                "member": member,
                "date": str(schedule_date),
                "title": title,
                "time": time
            })

            st.rerun()

with right:

    st.markdown("### 📋 선택 날짜 일정")

    selected_day = st.date_input(
        "조회 날짜",
        value=today,
        key="view"
    )

    events = [
        s for s in st.session_state.schedules
        if s["date"] == str(selected_day)
    ]

    if not events:
        st.info("일정이 없습니다 🌿")

    for event in events:

        color = member_colors[event["member"]]

        st.markdown(
            f"""
            <div style="
                background:{color};
                padding:12px;
                border-radius:12px;
                margin-bottom:10px;
            ">
            <b>{event["member"]}</b><br>
            📌 {event["title"]}<br>
            ⏰ {event["time"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"🗑️ 삭제",
            key=event["id"]
        ):
            st.session_state.schedules = [
                x for x in st.session_state.schedules
                if x["id"] != event["id"]
            ]
            st.rerun()
```
