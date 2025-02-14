import os
import requests
from github import Github

# 필요하다면 수정
ORG_NAME = "SSAFY-while-true"

def main():
    # GitHub Actions 환경 변수
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    if not GITHUB_TOKEN or not DISCORD_WEBHOOK_URL:
        print("Error: Missing GITHUB_TOKEN or DISCORD_WEBHOOK_URL")
        exit(1)

    # 지난 주, 이번 주 폴더명 계산 (원하면 이전주도 함께 체크 가능)
    prev_week, curr_week = get_previous_and_current_week()

    # 여기서는 '이번 주' 폴더만 확인한다고 가정
    # 필요하면 prev_week까지 함께 체크 로직을 추가하세요.
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

        # 기본값: X (미제출)
        status = "X"

        # 폴더 존재 여부 체크
        try:
            contents = repo.get_contents(target_week)
            # 폴더가 있다면 -> 제출로 간주
            # (필요시 contents 내 파일이 있는지 추가 검사 가능)
            status = "O"
        except:
            # 폴더가 없으면 그대로 X
            pass

        # 리스트에 "리포이름: O/X" 형식으로 저장
        results.append(f"{repo.name}: {status}")

    # 디스코드에 보낼 메시지
    # 예: "## 이번 주(YYYYMM_W) 제출 현황"
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
        print("Discord message sent successfully!")
    else:
        print(f"Failed to send Discord message. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
