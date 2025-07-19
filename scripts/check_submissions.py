import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from github import Github
from calculate_weeks import get_week_for_submission_check

ORG_NAME = "SSAFY-while-true"

def main():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    MATTERMOST_WEBHOOK_URL = os.getenv("MATTERMOST_WEBHOOK_URL")

    if not GITHUB_TOKEN:
        print("Error: Missing GITHUB_TOKEN")
        return

    # 방금 끝난 주차 계산 (제출 체크 대상)
    target_week = get_week_for_submission_check()
    print(f"DEBUG: Target week for submission check: {target_week}")

    # GitHub API
    gh = Github(GITHUB_TOKEN)
    org = gh.get_organization(ORG_NAME)

    report_lines = []
    report_lines.append("## 📊 Weekly Submissions Check")
    report_lines.append(f"**검사 대상 주차**: `{target_week}`\n")

    submission_results = []

    # 리포지토리 검사
    for repo in org.get_repos():
        # 숨김 리포 or 'infra' 포함 리포는 제외
        if repo.name.startswith(".") or "infra" in repo.name.lower():
            continue

        status = check_folder_and_files(repo, target_week)
        submission_results.append((repo.name, status))
        
        # 상태에 따라 이모지 추가
        emoji = "✅" if status == "O" else "❌"
        report_lines.append(f"{emoji} **{repo.name}**: {status}")

    # 통계 추가
    total_repos = len(submission_results)
    submitted_count = len([r for r in submission_results if r[1] == "O"])
    missing_count = total_repos - submitted_count
    
    report_lines.insert(2, f"**제출 현황**: {submitted_count}/{total_repos} ({missing_count}명 미제출)\n")

    final_message = "\n".join(report_lines)
    
    if missing_count > 0:
        final_message += f"\n\n☕ **미제출자 {missing_count}명** - 내일 커피 한 잔씩이에요! 😄"
    else:
        final_message += "\n\n🎉 **전원 제출 완료!** 모두 고생하셨습니다! 🔥"
    
    final_message += f"\n\n📅 다음 주 새로운 문제도 화이팅! 💪"

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
        print(f"DEBUG: Found folder {folder_name} in {repo.name}")
    except Exception as e:
        print(f"DEBUG: Folder {folder_name} not found in {repo.name}: {e}")
        return "X"

    valid_extensions = (".py", ".cpp", ".java", ".c", ".js", ".ts")
    
    for item in contents:
        if item.type == "file":
            print(f"DEBUG: Checking file {item.name} (size: {item.size}) in {repo.name}")
            
            # 확장자 검사 및 파일 크기 검사
            if item.name.lower().endswith(valid_extensions):
                if item.size > 0:  # 파일 크기가 0이 아닌 경우
                    print(f"DEBUG: Valid submission found: {item.name} in {repo.name}")
                    return "O"
            elif not item.name.lower().endswith((".md", ".txt", ".gitkeep")):
                # README, 메모 파일이 아닌 다른 파일도 제출로 인정
                if item.size > 0:
                    print(f"DEBUG: Valid submission found: {item.name} in {repo.name}")
                    return "O"
    
    print(f"DEBUG: No valid submissions found in {folder_name} for {repo.name}")
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
