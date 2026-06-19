
import streamlit as st
import sqlite3
import calendar
from datetime import date

# ----------------------------------
# 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="🏡 우리 가족 캘린더",
    page_icon="🏡",
    layout="wide"
)

# ----------------------------------
# 스타일
# ----------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.title-box {
    background: #faf7f2;
    border: 1px solid #e8e2d8;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# DB 연결
# ----------------------------------
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

# ----------------------------------
# 헤더
# ----------------------------------
st.markdown("""
<div class="title-box">
<h1>🏡 우리의 가족 캘린더</h1>
<p>신랑과 신부의 일정을 함께 공유해요</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# 일정 추가
# ----------------------------------
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
            ["🤵 창준", "👰 다영영"]
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

            st.success("일정이 저장되었습니다.")
            st.rerun()

# ----------------------------------
# 달력 년/월 선택
# ----------------------------------
today = date.today()

c1, c2 = st.columns(2)

with c1:
    year = st.selectbox(
        "연도",
        range(today.year - 2, today.year + 3),
        index=2
    )

with c2:
    month = st.selectbox(
        "월",
        range(1, 13),
        index=today.month - 1
    )

# ----------------------------------
# 일정 조회
# ----------------------------------
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

# ----------------------------------
# 달력
# ----------------------------------
st.subheader("📅 월간 일정")

weekdays = ["월", "화", "수", "목", "금", "토", "일"]

header = st.columns(7)

for i, day_name in enumerate(weekdays):
    header[i].markdown(f"**{day_name}**")

cal = calendar.Calendar(firstweekday=0)
weeks = cal.monthdayscalendar(year, month)

for week in weeks:

    cols = st.columns(7)

    for i, day in enumerate(week):

        with cols[i]:

            if day == 0:
                st.empty()
                continue

            current_date = date(year, month, day)
            key = str(current_date)

            with st.container(border=True):

                st.markdown(f"**{day}**")

                if key in events:

                    for _, member, title in events[key]:

                        if member == "🤵 신랑":
                            st.info(f"🤵 {title}")

                        else:
                            st.success(f"👰 {title}")

# ----------------------------------
# 등록된 일정 목록
# ----------------------------------
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

    col1, col2 = st.columns([6,1])

    with col1:
        st.write(
            f"{schedule_date} | {member} | {title}"
        )

    with col2:

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

