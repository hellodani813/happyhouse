import streamlit as st
from datetime import date
import uuid
import calendar
from datetime import datetime

# ----------------------------------
# 페이지 설정
# ----------------------------------

st.set_page_config(
    page_title="우리 가족 캘린더",
    page_icon="🌷",
    layout="wide"
)

# ----------------------------------
# 파스텔톤 스타일
# ----------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        180deg,
        #fff9fb 0%,
        #f7faff 100%
    );
}

.main-title{
    text-align:center;
    color:#6d7cff;
    font-size:3rem;
    font-weight:800;
    margin-bottom:0;
}

.sub-title{
    text-align:center;
    color:#8c8c8c;
    margin-bottom:30px;
}

.schedule-card{
    background:white;
    padding:16px;
    border-radius:18px;
    border:1px solid #ececec;
    box-shadow:0 3px 12px rgba(0,0,0,0.06);
    margin-bottom:12px;
}

.family-box{
    background:#ffffff;
    padding:20px;
    border-radius:20px;
    box-shadow:0 4px 14px rgba(0,0,0,0.06);
}

.member-tag{
    font-size:18px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# 세션 초기화
# ----------------------------------

if "schedules" not in st.session_state:
    st.session_state.schedules = []

# ----------------------------------
# 헤더
# ----------------------------------

st.markdown(
    "<div class='main-title'>🌷 우리 가족 캘린더 🌷</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>👨‍👩‍👧‍👦 가족 모두의 일정을 한눈에 관리해보세요</div>",
    unsafe_allow_html=True
)

# ----------------------------------
# 레이아웃
# ----------------------------------

left, right = st.columns([1, 1.4])

# ----------------------------------
# 일정 추가 영역
# ----------------------------------

with left:

    st.markdown("### ✨ 일정 추가")

    family_member = st.selectbox(
        "👤 가족 구성원",
        [
            "👨 아빠",
            "👩 엄마",
            "👦 첫째",
            "👧 둘째",
            "✨ 가족행사"
        ]
    )

    selected_date = st.date_input(
        "📅 날짜",
        value=date.today()
    )

    schedule_title = st.text_input(
        "📝 일정 제목",
        placeholder="예: 가족 외식"
    )

    schedule_time = st.text_input(
        "⏰ 시간",
        placeholder="예: 18:30"
    )

    memo = st.text_area(
        "💭 메모",
        placeholder="추가 메모를 입력하세요"
    )

    if st.button(
        "➕ 일정 추가",
        use_container_width=True
    ):

        if schedule_title.strip():

            st.session_state.schedules.append({
                "id": str(uuid.uuid4()),
                "member": family_member,
                "date": str(selected_date),
                "title": schedule_title,
                "time": schedule_time,
                "memo": memo
            })

            st.success("일정이 추가되었습니다 🌸")

        else:
            st.warning("일정 제목을 입력해주세요.")

# ----------------------------------
# 일정 보기
# ----------------------------------

with right:

    st.markdown("### 📅 일정 확인")

    view_date = st.date_input(
        "조회 날짜",
        value=date.today(),
        key="view_date"
    )

    schedules = [
        s
        for s in st.session_state.schedules
        if s["date"] == str(view_date)
    ]

    if not schedules:

        st.info("🌿 등록된 일정이 없습니다.")

    else:

        schedules.sort(key=lambda x: x["time"])

        for item in schedules:

            with st.container():

                st.markdown(
                    f"""
                    <div class='schedule-card'>
                        <div class='member-tag'>
                            {item["member"]}
                        </div>
                        <h4>📌 {item["title"]}</h4>
                        <p>⏰ {item["time"]}</p>
                        <p>💭 {item["memo"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"🗑️ 삭제",
                    key=item["id"]
                ):
                    st.session_state.schedules = [
                        s
                        for s in st.session_state.schedules
                        if s["id"] != item["id"]
                    ]
                    st.rerun()

# ----------------------------------
# 전체 일정
# ----------------------------------

st.divider()

st.markdown("### 🌈 전체 가족 일정")

if st.session_state.schedules:

    sorted_data = sorted(
        st.session_state.schedules,
        key=lambda x: (x["date"], x["time"])
    )

    for item in sorted_data:

        st.markdown(
            f"""
            <div class='schedule-card'>
            📅 <b>{item["date"]}</b>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            {item["member"]}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            ⏰ {item["time"]}

            <br><br>

            📌 <b>{item["title"]}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info("🌸 아직 등록된 일정이 없습니다.")

st.write("")
st.write("")

st.caption("💜 가족의 소중한 시간을 함께 관리해보세요")

def render_month_calendar(year, month, schedules):

    cal = calendar.monthcalendar(year, month)

    st.markdown("## 📅 월간 가족 캘린더")

    weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    cols = st.columns(7)

    for i, day in enumerate(weekdays):
        cols[i].markdown(
            f"<div style='text-align:center;font-weight:bold;color:#666'>{day}</div>",
            unsafe_allow_html=True
        )

    for week in cal:

        cols = st.columns(7)

        for idx, day in enumerate(week):

            if day == 0:
                cols[idx].markdown(
                    """
                    <div style='height:120px;border-radius:15px;background:#fafafa'></div>
                    """,
                    unsafe_allow_html=True
                )
                continue

            day_schedules = []

            for s in schedules:

                d = datetime.strptime(
                    s["date"],
                    "%Y-%m-%d"
                )

                if d.year == year and d.month == month and d.day == day:
                    day_schedules.append(s)

            html = f"""
            <div style="
                background:white;
                border-radius:15px;
                padding:8px;
                min-height:120px;
                border:1px solid #eee;
                box-shadow:0 2px 6px rgba(0,0,0,0.05);
            ">
            <b>{day}</b><br>
            """

            for item in day_schedules[:3]:

                html += f"""
                <div style="
                    background:#f4f0ff;
                    border-radius:8px;
                    padding:2px 6px;
                    margin-top:4px;
                    font-size:12px;
                ">
                {item["member"]}<br>
                {item["title"]}
                </div>
                """

            if len(day_schedules) > 3:
                html += f"<div style='font-size:12px'>+{len(day_schedules)-3}개 더</div>"

            html += "</div>"

            cols[idx].markdown(
                html,
                unsafe_allow_html=True
            )
