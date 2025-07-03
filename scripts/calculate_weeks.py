from datetime import datetime, timedelta

def calculate_week(year, month, day):
    """
    일요일을 기준으로 주차를 계산합니다.
    예: 2025년 7월 15일 → '202507_3'
    """
    date = datetime(year, month, day)
    first_day_of_month = date.replace(day=1)
    
    # 첫 날의 요일 (월=0, ..., 일=6)
    first_day_weekday = first_day_of_month.weekday()

    # 첫 번째 일요일 찾기
    if first_day_weekday != 6:
        first_sunday = first_day_of_month + timedelta(days=(6 - first_day_weekday))
    else:
        first_sunday = first_day_of_month
    
    # 주차 계산 (일요일이 포함된 주 기준)
    if date < first_sunday:
        week_number = 1
    else:
        week_number = ((date - first_sunday).days // 7) + 2  # 첫 주차는 1로 시작

    return f"{date.strftime('%Y%m')}_{week_number}"

def get_previous_and_current_week():
    """
    한국 시간 기준으로 지난주와 이번주 폴더명을 계산합니다.
    """
    # UTC + 9시간 (한국 시간)
    now = datetime.utcnow() + timedelta(hours=9)
    
    print(f"DEBUG: Current KST time: {now}")

    # 현재 주 계산 (기준점: 월요일 0시부터 일요일 23:59까지가 한 주)
    # 일요일(6)이면 이번 주로 계산
    # 월요일(0)~토요일(5)면 이번 주로 계산
    current_week = calculate_week(now.year, now.month, now.day)
    
    # 지난 주 계산 (7일 전)
    last_week_date = now - timedelta(days=7)
    previous_week = calculate_week(last_week_date.year, last_week_date.month, last_week_date.day)

    print(f"DEBUG: Previous week: {previous_week}, Current week: {current_week}")
    return previous_week, current_week

def get_current_week_for_reminder():
    """
    리마인더용 현재 주차 계산 (토요일 기준)
    토요일에는 다음 주 문제를 알려줌
    """
    now = datetime.utcnow() + timedelta(hours=9)
    
    # 토요일(5)이면 다음 주 폴더를 알려줌
    if now.weekday() == 5:  # 토요일
        next_week_date = now + timedelta(days=1)  # 일요일로 이동
        return calculate_week(next_week_date.year, next_week_date.month, next_week_date.day)
    else:
        return calculate_week(now.year, now.month, now.day)

if __name__ == "__main__":
    p, c = get_previous_and_current_week()
    print("지난 주:", p)
    print("이번 주:", c)
    
    reminder_week = get_current_week_for_reminder()
    print("리마인더 주차:", reminder_week)
