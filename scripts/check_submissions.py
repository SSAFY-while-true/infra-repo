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
    MATTERMOST_WEBHOOK_URL = os.getenv("MATTERMOST_WEBHOOK_URL")

    if not GITHUB_TOKEN:
        print("Error: Missing GITHUB_TOKEN")
        return

    # 지난주, 이번주 폴더 계산
    prev_week, curr_week = get_previous_and_current_week()

    # GitHub API
    gh = Github(GITHUB_TOKEN)
    org = gh.get_organization(ORG_NAME)

    report_lines = []
    report_lines.append("## Weekly Submissions Check")
    report_lines.append(f"- 지난 주 폴더: `{prev_week}`, 이번 주 폴더: `{curr_week}`\n")

    # 리포지토리 검사
    for repo in org.get_repos():
        # 숨김 리포 or 'infra' 포함 리포는 제외
        if repo.name.startswith(".") or "infra" in repo.name.lower():
            continue

        prev_status = check_folder_and_files(repo, prev_week)
        curr_status = check_folder_and_files(repo, curr_week)

        report_lines.append(
            f"**{repo.name}**: 지난주 {prev_status} / 이번주 {curr_status}"
        )

    final_message = "\n".join(report_lines)
    final_message += "\n\n이번 주도 모두 수고 많으셨습니다!\n"
    final_message += "**X**로 표시된 분들은 내일 바나프레소 커피… 부탁드립니다!"

    # 웹훅 전송
    if DISCORD_WEBHOOK_URL:
        send_to_discord(DISCORD_WEBHOOK_URL, final_message)
    if MATTERMOST_WEBHOOK_URL:
        send_to_mattermost(MATTERMOST_WEBHOOK_URL, final_message)

def check_folder_and_files(repo, folder_name):
    """
    폴더 + 파일 유무 체크
    - 폴더가 없으면 X
    - 폴더가 있어도 제출 파일(.py, .cpp, .java 등)이 없으면 X
    - 0바이트(빈 파일)인 경우 제출 인정하지 않음
    """
    try:
        contents = repo.get_contents(folder_name)
    except:
        return "X"

    for item in contents:
        if item.type == "file":
            # 확장자 검사
            if item.name.lower().endswith((".py", ".cpp", ".java")):
                if item.size > 0:  # 파일 크기가 0이 아닌 경우
                    return "O"
            elif not item.name.lower().endswith(".md"):
                if item.size > 0:
                    return "O"
    return "X"

def send_to_discord(webhook_url, message):
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code in [200, 204]:
            print("Discord message sent successfully!")
        else:
            print(f"Failed to send Discord message. Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def send_to_mattermost(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Mattermost message sent successfully!")
        else:
            print(f"Failed to send Mattermost message. Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending Mattermost message: {e}")

if __name__ == "__main__":
    main()
