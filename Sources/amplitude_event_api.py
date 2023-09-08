import requests
import base64
import json
import os
from urllib.parse import urlencode

def fetch_event_segmentation(event_type, start_date, end_date, i=1):
    # Base64 인코딩
    api_key=os.environ.get('AMPLITUDE_API_KEY')
    secret_key=os.environ.get('AMPLITUDE_SECRET_KEY')
    credentials = base64.b64encode(f"{api_key}:{secret_key}".encode("utf-8")).decode("utf-8")

    # 이벤트 타입을 JSON 형식으로 인코딩
    event_data = json.dumps({"event_type": event_type})

    # URL 인코딩
    params = {
        'e': event_data,
        'start': start_date,
        'end': end_date
    }
    url_params = urlencode(params)

    # API URL
    url = f"https://amplitude.com/api/2/events/segmentation?{url_params}"

    # HTTP GET 요청
    try:
        response = requests.get(
            url,
            headers={
                "Authorization": f"Basic {credentials}"
            },
            timeout=5
        )

    except requests.exceptions.Timeout:
        print("The request timed out.")

    # 응답 처리
    if response.status_code == 200:
        return response.json()

    return f"Failed: {response.status_code}, {response.text}"
