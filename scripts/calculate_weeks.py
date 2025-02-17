from datetime import datetime, timedelta

def calculate_week(year, month, day):
    """
    월요일을 기준으로 주차를 계산합니다.
    예: 2024년 2월 15일 → '202402_3'
    """
    date = datetime(year, month, day)
    first_day_of_month = date.replace(day=1)
    monday = date - timedelta(days=date.weekday())
    week_number = ((monday - first_day_of_month).days // 7) + 1

    return f"{date.strftime('%Y%m')}_{week_number}"

def get_previous_and_current_week():
    # 한국 시간(UTC+9)을 고려
    now = datetime.utcnow() + timedelta(hours=9)

    # 언제 실행되든 동일한 기준으로 주차 계산
    # 일요일에 실행되었을 경우, 토요일 날짜로 고정
    # 월요일에 실행되었을 경우, 일요일 -> 토요일로 변경
    # GitHub Actions는 지정된 cron 시간에 정확히 실행되지 않고 약 10 ~ 30분 정도 지연되기 때문
    if now.weekday() == 6:        # 현재가 일요일이면, 토요일 날짜로 계산
        now = now - timedelta(days=1)
    elif now.weekday() == 0:        # 현재가 월요일이면, 이틀 전(토요일)로 계산
        now = now - timedelta(days=2)
        
    current_week = calculate_week(now.year, now.month, now.day)
    last_week = now - timedelta(days=7)
    previous_week = calculate_week(last_week.year, last_week.month, last_week.day)

    return previous_week, current_week

if __name__ == "__main__":
    p, c = get_previous_and_current_week()
    print("지난 주:", p)
    print("이번 주:", c)
