import os
import requests
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from github import Github
from calculate_weeks import get_previous_and_current_week

ORG_NAME = "SSAFY-while-true"

def main():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    if not GITHUB_TOKEN or not DISCORD_WEBHOOK_URL:
        print("❌ Error: Missing GITHUB_TOKEN or DISCORD_WEBHOOK_URL")
        exit(1)

    # 지난주, 이번주 주차 폴더 계산
    prev_week, curr_week = get_previous_and_current_week()

    # PyGithub로 오가나이제이션 객체 가져오기
    gh = Github(GITHUB_TOKEN)
    org = gh.get_organization(ORG_NAME)

    # 보고용 문자열 리스트
    report_lines = []
    # 헤더 메시지
    report_lines.append("## 📝 Weekly Submissions Check")
    report_lines.append(f"- 지난 주 폴더: `{prev_week}`, 이번 주 폴더: `{curr_week}`\n")

    # 모든 리포지토리 순회
    repos = org.get_repos()
    for repo in repos:
        # 숨김 리포(.github 등) 제외
        if repo.name.startswith("."):
            continue
        # infra 리포제거
        if "infra" in repo.name.lower():
            continue

        # 지난주와 이번주 폴더 체크
        prev_status = check_folder_and_files(repo, prev_week)
        curr_status = check_folder_and_files(repo, curr_week)

        report_lines.append(
            f"**{repo.name}**: 지난주 {prev_status} / 이번주 {curr_status}"
        )

    # 본문 메시지
    final_message = "\n".join(report_lines)
    final_message += "\n\n이번 주도 모두 수고 많으셨습니다! 🔥\n"
    final_message += "**X**로 표시된 분들은 내일 바나프레소 커피… ☕ 약속이죠? 😆"

    # 디스코드 웹훅 전송
    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": final_message}
    )
    if response.status_code == 204:
        print("✅ Discord message sent successfully!")
    else:
        print(f"❌ Failed to send Discord message. Status Code: {response.status_code}")
        print(response.text)

def check_folder_and_files(repo, folder_name):
    """
    폴더 + 파일 유무 체크
    - 폴더가 없으면 X
    - 폴더가 있어도 제출 파일(.py, .cpp, .java 등)이 없으면 X
    - 하나라도 제출 파일이 있으면 O
    """
    try:
        contents = repo.get_contents(folder_name)
    except:
        # 폴더 자체 없음
        return "X"

    # 폴더가 존재하므로 내부 파일 체크
    code_file_found = False
    for item in contents:
        if item.type == "file":
            # 확장자 필터 (예: .py, .cpp, .java)
            if item.name.lower().endswith((".py", ".cpp", ".java")):
                code_file_found = True
                break
            # .md만 있는 경우 제출로 보기 싫다면 처리
            if not item.name.lower().endswith(".md"):
                code_file_found = True
                break

        # 하위 폴더가 또 있을 수 있다면 재귀적으로 검색 가능

    return "O" if code_file_found else "X"

if __name__ == "__main__":
    main()
