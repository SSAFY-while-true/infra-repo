from datetime import datetime, timedelta

def calculate_week(year, month, day):
    """
    - 월요일 기준 주차 계산
    - 2024년 2월 15일 → '202402_3'
    """
    date = datetime(year, month, day)

    first_day_of_month = date.replace(day=1)
    monday = date - timedelta(days=date.weekday())  # 이 주의 월요일
    week_number = ((monday - first_day_of_month).days // 7) + 1

    return f"{date.strftime('%Y%m')}_{week_number}"

def get_previous_and_current_week():
    today = datetime.utcnow() + timedelta(hours=9)  # 한국 시간 고려
    current_week = calculate_week(today.year, today.month, today.day)

    last_week_date = today - timedelta(days=7)
    previous_week = calculate_week(last_week_date.year,
                                   last_week_date.month,
                                   last_week_date.day)

    return previous_week, current_week