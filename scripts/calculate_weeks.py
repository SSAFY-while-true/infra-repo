from datetime import datetime, timedelta

def calculate_week(target_date):
    """
    월요일 기준 주차 계산 (언제나 작동)
    해당 주의 월요일이 속한 달을 기준으로 폴더명 생성
    
    예: 
    - 2025년 7월 1일(화) → 월요일은 6월 30일 → 202506_5
    - 2025년 7월 7일(월) → 202507_2
    - 2025년 7월 14일(월) → 202507_3
    - 2025년 8월 4일(월) → 202508_2
    """
    
    # 해당 주의 월요일 찾기
    monday_of_week = target_date - timedelta(days=target_date.weekday())
    
    # 월요일이 속한 달의 1일
    first_day_of_month = monday_of_week.replace(day=1)
    
    # 그 달의 첫 번째 월요일 찾기
    first_monday_of_month = first_day_of_month
    if first_day_of_month.weekday() != 0:  # 월요일이 아니면
        days_to_monday = 7 - first_day_of_month.weekday()
        first_monday_of_month = first_day_of_month + timedelta(days=days_to_monday)
    
    # 해당 월의 몇 번째 주인지 계산 (1부터 시작)
    week_in_month = ((monday_of_week - first_monday_of_month).days // 7) + 1
    
    return f"{monday_of_week.strftime('%Y%m')}_{week_in_month}"

def get_previous_and_current_week():
    """
    한국 시간 기준으로 지난주와 이번주 폴더명을 계산합니다.
    """
    # UTC + 9시간 (한국 시간)
    now = datetime.utcnow() + timedelta(hours=9)
    
    print(f"DEBUG: Current KST time: {now}")
    
    # 현재 주 계산
    current_week = calculate_week(now)
    
    # 지난 주 계산 (7일 전)
    last_week_date = now - timedelta(days=7)
    previous_week = calculate_week(last_week_date)

    print(f"DEBUG: Previous week: {previous_week}, Current week: {current_week}")
    return previous_week, current_week

def get_current_week_for_reminder():
    """
    리마인더용 주차 계산
    토요일에도 현재 주차 반환 (일요일까지 제출하세요 의미)
    """
    now = datetime.utcnow() + timedelta(hours=9)
    return calculate_week(now)

def get_week_for_notion_reminder():
    """
    노션 문제 출제 리마인더용 주차 계산 (수요일 실행)
    """
    now = datetime.utcnow() + timedelta(hours=9)
    return calculate_week(now)

# 테스트 함수
def test_week_calculation():
    """다양한 경계 상황 테스트"""
    test_cases = [
        "2025-07-01",  # 화요일 (월요일은 6월 30일)
        "2025-07-07",  # 월요일 (7월 첫 월요일)
        "2025-07-14", # 월요일 (7월 둘째 월요일)
        "2025-08-03", # 일요일 (월요일은 7월 28일)
        "2025-08-04", # 월요일 (8월 첫 월요일)
    ]
    
    print("=== 주차 계산 테스트 ===")
    for date_str in test_cases:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        result = calculate_week(date)
        monday = date - timedelta(days=date.weekday())
        print(f"{date_str} ({date.strftime('%a')}) → 월요일: {monday.strftime('%Y-%m-%d')} → {result}")

if __name__ == "__main__":
    try:
        # 현재 상황 출력
        p, c = get_previous_and_current_week()
        print("지난 주:", p)
        print("이번 주:", c)
        
        reminder_week = get_current_week_for_reminder()
        print("리마인더 주차:", reminder_week)
        
        notion_week = get_week_for_notion_reminder()
        print("노션 리마인더 주차:", notion_week)
        
        print()
        test_week_calculation()
        
    except Exception as e:
        print(f"Error: {e}")
