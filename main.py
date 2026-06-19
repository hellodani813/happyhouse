import streamlit as st
import sqlite3
import calendar
from datetime import date

# ------------------
# 설정
# ------------------

st.set_page_config(
    page_title="우리 가족 캘린더",
    page_icon="🏡",
    layout="wide"
)

# ------------------
# 스타일
# ------------------

st.markdown("""
<style>

.main {
    background-color: #f7f4ef;
}

.title-box {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #ece6dd;
    text-align: center;
    margin-bottom: 20px;
}

.calendar-cell {
    border: 1px solid #ece6dd;
    border-radius: 12px;
    padding: 8px;
    min-height: 150px;
    background: white;
}

.day-number {
    font-weight: bold;
    margin-bottom: 8px;
}

.husband {
    background: #dbeafe;
    padding: 4px;
    border-radius: 8px;
    margin-bottom: 4px;
    font-size: 12px;
}

.wife {
    background: #ffe4e6;
    padding: 4px;
    border-radius: 8px;
    margin-bottom: 4px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------
# DB
# ------------------

conn = sqlite3.connect("family_calendar.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedules(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_date TEXT,
    member TEXT,
    title TEXT
)
""")

conn.commit()

# ------------------
# 헤더
# ------------------

st.markdown("""
<div class="title-box">
<h1>🏡 우리의 가족 캘린더</h1>
<p>신랑과 신부의 일정을 함께 공유해요</p>
</div>
""", unsafe_allow_html=True)

# ------------------
# 일정 등록
# ------------------

with st.expander("➕ 일정 추가", expanded=True):

    col1, col2, col3 = st.columns([1,1,2])

    with col1:
        schedule_date = st.date_input(
            "날짜",
            value=date.today()
        )

    with col2:
        member = st.selectbox(
            "구성원",
            ["🤵 신랑", "👰 신부"]
        )

    with col3:
        title = st.text_input("일정")

    if st.button("저장", use_container_width=True):

        if title.strip():

            cursor.execute(
                """
                INSERT INTO schedules
                (schedule_date, member, title)
                VALUES (?, ?, ?)
                """,
                (
                    str(schedule_date),
                    member,
                    title
                )
            )

            conn.commit()

            st.success("저장 완료!")
            st.rerun()

# ------------------
# 달력 선택
# ------------------

today = date.today()

c1, c2 = st.columns(2)

with c1:
    year = st.selectbox(
        "연도",
        list(range(today.year - 2, today.year + 3)),
        index=2
    )

with c2:
    month = st.selectbox(
        "월",
        list(range(1,13)),
        index=today.month - 1
    )

# ------------------
# 일정 조회
# ------------------

cursor.execute("SELECT * FROM schedules")
rows = cursor.fetchall()

events = {}

for row in rows:

    event_id = row[0]
    event_date = row[1]
    member = row[2]
    title = row[3]

    if event_date not in events:
        events[event_date] = []

    events[event_date].append(
        (event_id, member, title)
    )

# ------------------
# 달력
# ------------------

st.subheader("📅 월간 일정")

week_names = ["월","화","수","목","금","토","일"]

header_cols = st.columns(7)

for i, day in enumerate(week_names):
    header_cols[i].markdown(
        f"**{day}**"
    )

cal = calendar.Calendar(firstweekday=0)

weeks = cal.monthdayscalendar(year, month)

for week in weeks:

    cols = st.columns(7)

    for i, day in enumerate(week):

        with cols[i]:

            if day == 0:
                st.write("")
                continue

            current = date(year, month, day)

            key = str(current)

            html = f"""
            <div class='calendar-cell'>
            <div class='day-number'>{day}</div>
            """

            if key in events:

                for _, member, title in events[key]:

                    cls = (
                        "husband"
                        if member == "🤵 신랑"
                        else "wife"
                    )

                    html += f"""
                    <div class='{cls}'>
                    {member}<br>
                    {title}
                    </div>
                    """

            html += "</div>"

            st.markdown(
                html,
                unsafe_allow_html=True
            )

# ------------------
# 일정 관리
# ------------------

st.divider()
st.subheader("📝 등록된 일정")

cursor.execute("""
SELECT *
FROM schedules
ORDER BY schedule_date
""")

rows = cursor.fetchall()

if not rows:
    st.info("등록된 일정이 없습니다.")

for row in rows:

    event_id = row[0]
    schedule_date = row[1]
    member = row[2]
    title = row[3]

    c1, c2 = st.columns([6,1])

    with c1:
        st.write(
            f"{schedule_date} | {member} | {title}"
        )

    with c2:

        if st.button(
            "삭제",
            key=f"delete_{event_id}"
        ):

            cursor.execute(
                "DELETE FROM schedules WHERE id=?",
                (event_id,)
            )

            conn.commit()

            st.rerun()
