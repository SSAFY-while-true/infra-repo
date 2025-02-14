import os
import requests
from github import Github
from datetime import datetime, timedelta

# 필요하다면 수정
ORG_NAME = "SSAFY-while-true"

def calculate_week(year, month, day):
    """
    이번 주가 몇 번째 주인지 계산하는 함수
    - 월요일 기준으로 주차 계산
    - 예: 2024년 2월 15일이면 → '202402_3'
    """
    date = datetime(year, month, day)

    # 해당 날짜가 속한 월의 첫 날 찾기
    first_day_of_month = date.replace(day=1)

    # 이번 주의 월요일 찾기
    monday = date - timedelta(days=date.weekday())

    # 주차 계산 (해당 월 기준)
    week_number = ((monday - first_day_of_month).days // 7) + 1

    return f"{date.strftime('%Y%m')}_{week_number}"

def get_previous_and_current_week():
    """
    - 지난 주와 이번 주의 폴더명을 반환하는 함수
    - GitHub Actions에서 실행되므로 항상 실행 날짜 기준으로 계산
    """
    today = datetime.today()

    current_week = calculate_week(today.year, today.month, today.day)

    last_week_date = today - timedelta(days=7)
    previous_week = calculate_week(last_week_date.year, last_week_date.month, last_week_date.day)

    return previous_week, current_week

def main():
    # GitHub Actions 환경 변수
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    if not GITHUB_TOKEN or not DISCORD_WEBHOOK_URL:
        print("Error: Missing GITHUB_TOKEN or DISCORD_WEBHOOK_URL")
        exit(1)

    # 주차 폴더명 계산
    prev_week, curr_week = get_previous_and_current_week()

    # 현재 주차를 기준으로 검사 (필요시 prev_week 추가 가능)
    target_week = curr_week

    # 깃허브 인증 & 오가나이제이션 객체 가져오기
    gh = Github(GITHUB_TOKEN)
    org = gh.get_organization(ORG_NAME)

    # 결과 저장용 리스트
    results = []

    # 오가나이제이션 내 모든 리포지토리 순회
    for repo in org.get_repos():
        # 예: .github 레포, demo-repo 등 스킵할 수도 있음
        if repo.name.startswith("."):
            continue
        elif repo.name in ["infra-repo", ".github"]:
            continue

        # 기본값: X (미제출)
        status = "X"

        # 폴더 존재 여부 체크
        try:
            contents = repo.get_contents(target_week)
            # 폴더가 있다면 → 제출로 간주
            status = "O"
        except:
            # 폴더가 없으면 그대로 X
            pass

        # 리스트에 "리포이름: O/X" 형식으로 저장
        results.append(f"{repo.name}: {status}")

    # 디스코드에 보낼 메시지
    message_lines = []
    message_lines.append(f"## 🔎 Week [{target_week}] Submission Check\n")
    for line in results:
        message_lines.append(line)

    # 최종 메시지
    final_message = "\n".join(message_lines)

    # 디스코드 웹훅 전송
    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": final_message}
    )

    if response.status_code == 204:
        print("✅ Discord message sent successfully!")
    else:
        print(f"❌ Failed to send Discord message. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
