from datetime import datetime, timedelta

def calculate_week(target_date):
    """
    2025년 7월 14일(월)을 기준으로 주차를 계산합니다.
    일요일이 주의 마지막 날이며, 월요일이 새 주의 시작입니다.
    연속성을 보장하여 중복 없는 고유한 폴더명을 생성합니다.
    
    예: 
    - 2025년 7월 14일(월) ~ 7월 20일(일) → 202507_3
    - 2025년 7월 21일(월) ~ 7월 27일(일) → 202507_4
    - 2025년 7월 28일(월) ~ 8월 3일(일) → 202507_5 (월 경계를 넘어도 7월 기준)
    """
    
    # 스터디 시작 기준점: 2025년 7월 14일(월)
    study_start = datetime(2025, 7, 14)  # 월요일
    
    # 기준점 이전이면 에러
    if target_date < study_start:
        raise ValueError(f"스터디 시작일({study_start.strftime('%Y-%m-%d')}) 이전입니다.")
    
    # 스터디 시작일로부터 몇 주 지났는지 계산
    days_diff = (target_date - study_start).days
    week_number = (days_diff // 7) + 3  # 7월 3주차부터 시작
    
    # 폴더명은 해당 주의 월요일 기준으로 결정
    monday_of_week = target_date - timedelta(days=target_date.weekday())
    
    return f"{monday_of_week.strftime('%Y%m')}_{week_number}"

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
    토요일에는 일요일까지 포함된 현재 주차를 알려줌 (다음 주가 아님)
    """
    now = datetime.utcnow() + timedelta(hours=9)
    
    # 모든 요일에서 현재 주차 반환
    # 토요일 리마인더는 "일요일까지 제출하세요"라는 의미이므로 현재 주차가 맞음
    return calculate_week(now)

def get_week_for_notion_reminder():
    """
    노션 문제 출제 리마인더용 주차 계산 (수요일 실행)
    수요일에 이번 주 문제를 출제하라고 알림
    """
    now = datetime.utcnow() + timedelta(hours=9)
    return calculate_week(now)

# 테스트 함수들
def test_week_calculation():
    """주요 날짜들에 대한 테스트"""
    test_dates = [
        (datetime(2025, 7, 14), "202507_3"),  # 스터디 시작일 (월)
        (datetime(2025, 7, 20), "202507_3"),  # 첫 주 일요일
        (datetime(2025, 7, 21), "202507_4"),  # 둘째 주 월요일
        (datetime(2025, 7, 27), "202507_4"),  # 둘째 주 일요일
        (datetime(2025, 8, 3), "202507_5"),   # 월 경계 넘어가는 주 일요일
        (datetime(2025, 8, 4), "202508_6"),   # 새 달 시작 주 월요일
    ]
    
    print("=== 주차 계산 테스트 ===")
    for date, expected in test_dates:
        result = calculate_week(date)
        status = "✅" if result == expected else "❌"
        print(f"{date.strftime('%Y-%m-%d (%a)')}: {result} {status}")
        
def test_current_scenario():
    """현재 시나리오 테스트"""
    print("\n=== 현재 시나리오 테스트 ===")
    
    # 이번 주 시뮬레이션
    test_dates = [
        datetime(2025, 7, 3),   # 목요일 (오늘)
        datetime(2025, 7, 5),   # 토요일 (리마인더)
        datetime(2025, 7, 6),   # 일요일 (체크)
    ]
    
    for date in test_dates:
        week = calculate_week(date)
        print(f"{date.strftime('%Y-%m-%d (%a)')}: {week}")

if __name__ == "__main__":
    # 기존 함수 실행
    try:
        p, c = get_previous_and_current_week()
        print("지난 주:", p)
        print("이번 주:", c)
        
        reminder_week = get_current_week_for_reminder()
        print("리마인더 주차:", reminder_week)
        
        notion_week = get_week_for_notion_reminder()
        print("노션 리마인더 주차:", notion_week)
        
        # 테스트 실행
        test_week_calculation()
        test_current_scenario()
        
    except Exception as e:
        print(f"Error: {e}")
        print("스터디가 아직 시작하지 않았거나 날짜가 잘못되었습니다.")
