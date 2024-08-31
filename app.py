import streamlit as st
import pandas as pd
import datetime
import calendar
import random

# 마라톤 일정 데이터 (대한민국 전체 마라톤 일정 예시)
marathons = [
    {"date": "2024-03-17", "name": "서울국제마라톤", "location": "서울", "link": "https://marathon-korea.com/events/seoul-international-marathon", "song": "https://marathon-korea.com/music/born_to_run.mp3"},
    {"date": "2024-04-14", "name": "대구국제마라톤", "location": "대구", "link": "https://marathon-korea.com/events/daegu-international-marathon", "song": "https://marathon-korea.com/music/run_the_world.mp3"},
    {"date": "2024-05-26", "name": "경주마라톤", "location": "경주", "link": "https://marathon-korea.com/events/gyeongju-marathon", "song": "https://marathon-korea.com/music/running_on_empty.mp3"},
    {"date": "2024-06-02", "name": "부산록마라톤", "location": "부산", "link": "https://marathon-korea.com/events/busan-rock-marathon", "song": "https://marathon-korea.com/music/i_gotta_feeling.mp3"},
    {"date": "2024-07-21", "name": "제주마라톤", "location": "제주", "link": "https://marathon-korea.com/events/jeju-marathon", "song": "https://marathon-korea.com/music/island_in_the_sun.mp3"},
    {"date": "2024-09-08", "name": "인천마라톤", "location": "인천", "link": "https://marathon-korea.com/events/incheon-marathon", "song": "https://marathon-korea.com/music/cant_stop_the_feeling.mp3"},
    {"date": "2024-10-20", "name": "춘천마라톤", "location": "춘천", "link": "https://marathon-korea.com/events/chuncheon-marathon", "song": "https://marathon-korea.com/music/eye_of_the_tiger.mp3"},
    {"date": "2024-11-03", "name": "광주마라톤", "location": "광주", "link": "https://marathon-korea.com/events/gwangju-marathon", "song": "https://marathon-korea.com/music/dont_stop_me_now.mp3"}
]

# 오늘 날짜와 현재 월 설정
today = datetime.date.today()
current_year = today.year
current_month = today.month

# 마라톤 데이터프레임 생성
df = pd.DataFrame(marathons)

# 마라톤 리스트 필터링 함수
def filter_marathons_by_month(year, month):
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])
    return df[(pd.to_datetime(df['date']).dt.date >= start_date) & (pd.to_datetime(df['date']).dt.date <= end_date)]

# Streamlit UI
st.set_page_config(page_title="대한민국 마라톤 일정", page_icon="🏃", layout="wide")

st.title("대한민국 마라톤 일정")

# 달력과 이벤트 섹션
col1, col2 = st.columns([1, 2])

with col1:
    st.header(f"{current_year}년 {current_month}월 달력")
    st.write("**마라톤 일정이 있는 날짜는 노란색으로 표시됩니다.**")
    
    # 달력 출력
    calendar_text = calendar.TextCalendar(calendar.SUNDAY).formatmonth(current_year, current_month)
    st.markdown(f"```{calendar_text}```")

    # 마라톤 이벤트 날짜 표시
    marathons_this_month = filter_marathons_by_month(current_year, current_month)
    if not marathons_this_month.empty:
        for _, row in marathons_this_month.iterrows():
            event_date = pd.to_datetime(row['date']).date()
            st.markdown(f"- **{row['name']}** ({event_date}) [{row['location']}]({row['link']})")

with col2:
    st.header("전체 마라톤 일정")
    
    # 마라톤 리스트 출력
    for _, row in df.iterrows():
        event_date = pd.to_datetime(row['date']).date()
        if event_date >= today:
            st.write(f"### {row['name']}")
            st.write(f"- 날짜: {event_date}")
            st.write(f"- 장소: {row['location']}")
            st.write(f"- [상세 정보]({row['link']})")
            if st.button(f"{row['name']} 테마곡 재생"):
                st.audio(row['song'])

# 이전/다음 달 이동 버튼
prev_col, next_col = st.columns([1, 1])

with prev_col:
    if st.button("이전 달"):
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1

with next_col:
    if st.button("다음 달"):
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1
