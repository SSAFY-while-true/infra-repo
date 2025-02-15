import os
import requests
import sys
import os
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

    # 이번 주 폴더명 계산
    _, curr_week = get_previous_and_current_week()

    # 디스코드로 보낼 메시지
    reminder_message = (
        f"🔔 **Reminder!** 🔔\n\n"
        f"이번 주 폴더명은 `{curr_week}` 입니다.\n"
        f"문제 풀이 & 폴더 업로드 잊지 마세요! 💪\n"
        f"모두 화이팅입니다! 🚀"
    )

    # 디스코드 웹훅 전송
    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": reminder_message}
    )

    if response.status_code == 204:
        print("✅ Reminder message sent successfully!")
    else:
        print(f"❌ Failed to send reminder. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()