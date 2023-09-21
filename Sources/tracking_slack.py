import json
import requests
import os

SLACK_WEBHOOK_URL = os.environ.get('AMPLITUDE_SLACK_WEBHOOK_URL')

def send_to_slack(text: str) -> None:
    """
    Slack으로 텍스트 메시지를 전송하는 함수
    
    Parameters:
    - text (str): 전송할 메시지 내용
    - slack_webhook_url (str): Slack Webhook URL
    
    Returns:
    - None
    """
    # 메시지 내용 구성
    message = {
        "text": text
    }

    # Slack으로 POST 요청 보내기
    response = requests.post(
        os.environ.get('AMPLITUDE_SLACK_WEBHOOK_URL'),
        data=json.dumps(message),
        headers={'Content-Type': 'application/json'},
        timeout=5  # 5초 동안 응답이 없으면 타임아웃
    )

    # 응답 확인
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Reason: {response.text}")

def send_slack_message_with_payload(payload):
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    return response.status_code == 200
