import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from calculate_weeks import get_previous_and_current_week

def main():
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    MATTERMOST_WEBHOOK_URL = os.getenv("MATTERMOST_WEBHOOK_URL")

    # 이번 주 폴더 계산
    _, curr_week = get_previous_and_current_week()
    
    # 현재 주차를 기준으로 조 결정
    # 예: 202507_3 → 3주차 → 홀수주차 → 1조
    week_number = int(curr_week.split('_')[1])
    if week_number % 2 == 1:  # 홀수 주차
        assigned_team = "1조 (김서현, 신범수, 이현석)"
    else:  # 짝수 주차
        assigned_team = "2조 (김미진, 조영우, 홍훈)"
    
    # 노션 링크
    notion_link = "https://slender-chime-b9f.notion.site/198f0459a9028029bd9cd1f000cfcab8?pvs=74"
    
    # 메시지 작성
    reminder_message = (
        f"📝 **문제 출제 리마인더** 📝\n\n"
        f"🗓️ **이번 주차**: `{curr_week}`\n"
        f"👥 **출제 담당**: {assigned_team}\n"
        f"🎯 **SQL 담당**: 박민수\n\n"
        f"⏰ **마감 시간**: 오늘(수요일) 자정 23:59분까지\n"
        f"📍 **업로드 위치**: [노션 페이지]({notion_link})\n\n"
        f"✅ **출제 내용**:\n"
        f"- 알고리즘 문제 3개 (담당 조)\n"
        f"- SQL 문제 1개 (박민수)\n\n"
        f"담당 조와 박민수님, 문제 출제 부탁드립니다! 💪\n"
        f"늦지 않게 올려주세요~ 🚀"
    )

    # 웹훅 전송
    if DISCORD_WEBHOOK_URL:
        send_to_discord(DISCORD_WEBHOOK_URL, reminder_message)
    if MATTERMOST_WEBHOOK_URL:
        send_to_mattermost(MATTERMOST_WEBHOOK_URL, reminder_message)

def send_to_discord(webhook_url, message):
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code in [200, 204]:
            print("Discord notion reminder sent successfully!")
        else:
            print(f"Failed to send Discord notion reminder. Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord notion reminder: {e}")

def send_to_mattermost(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Mattermost notion reminder sent successfully!")
        else:
            print(f"Failed to send Mattermost notion reminder. Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending Mattermost notion reminder: {e}")

if __name__ == "__main__":
    main()