import os
import requests
from github import Github
from calculate_weeks import get_previous_and_current_week
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# GitHub 오가나이제이션 이름
ORG_NAME = "SSAFY-while-true"

def main():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    if not GITHUB_TOKEN or not DISCORD_WEBHOOK_URL:
        print("❌ Error: Missing GITHUB_TOKEN or DISCORD_WEBHOOK_URL")
        exit(1)

    # 지난주, 이번주 주차 폴더 구하기
    prev_week, curr_week = get_previous_and_current_week()

    # GitHub API (PyGithub)
    gh = Github(GITHUB_TOKEN)
    org = gh.get_organization(ORG_NAME)

    # 보고용 문자열
    report_lines = []
    report_lines.append(f"## 📝 Weekly Submissions Check")
    report_lines.append(f"- 지난 주 폴더: `{prev_week}`, 이번 주 폴더: `{curr_week}`\n")

    repos = org.get_repos()
    for repo in repos:
        # .github 등 숨김/특수 리포지토리는 제외하고 싶으면 조건 추가
        if repo.name.startswith("."):
            continue

        # 지난 주 폴더 검사
        prev_status = check_folder_and_files(repo, prev_week)

        # 이번 주 폴더 검사
        curr_status = check_folder_and_files(repo, curr_week)

        # 예: "**ppower-dev**: 지난주 X / 이번주 O" 식의 줄을 추가
        report_lines.append(f"**{repo.name}**: 지난주 {prev_status} / 이번주 {curr_status}")

    final_message = "\n".join(report_lines)

    # 디스코드로 메시지 전송
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": final_message})
    if response.status_code == 204:
        print("✅ Discord message sent successfully!")
    else:
        print(f"❌ Failed to send Discord message. Status Code: {response.status_code}")
        print(response.text)

def check_folder_and_files(repo, folder_name):
    """
    - 폴더가 없으면 'X'
    - 폴더가 있어도 코드(파일)가 없으면 'X'
    - 하나라도 파일(코드)이 있으면 'O'
    
    원한다면 파일 확장자(.py, .cpp 등) 필터링도 가능.
    """
    try:
        contents = repo.get_contents(folder_name)
    except:
        # 폴더 자체가 없으면 미제출
        return "X"

    # 폴더가 존재하긴 하므로, 내부 파일이 있는지 체크
    code_file_found = False

    for item in contents:
        if item.type == "file":
            # 필요하다면 확장자 체크 (예: .py, .cpp 등)
            if item.name.lower().endswith((".py", ".cpp", ".java")):
                code_file_found = True
                break

            # 또는 그냥 README.md만 빼고, 나머지는 전부 제출 파일로 간주
            if not item.name.lower().endswith(".md"):
                code_file_found = True
                break

        # 만약 폴더 안에 또 폴더가 있을 수 있다면?
        # (item.type == "dir") -> 재귀적으로 파일 검색하는 로직 추가도 가능.

    return "O" if code_file_found else "X"

if __name__ == "__main__":
    main()
