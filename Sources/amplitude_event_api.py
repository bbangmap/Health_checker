import requests
import base64
import json
import os
from urllib.parse import urlencode
from urllib.parse import quote

def fetch_event_segmentation(event_type, start_date, end_date, i=1, m="uniques", group_by=None):
    # Base64 인코딩
    api_key=os.environ.get('AMPLITUDE_API_KEY')
    secret_key=os.environ.get('AMPLITUDE_SECRET_KEY')
    credentials = base64.b64encode(f"{api_key}:{secret_key}".encode("utf-8")).decode("utf-8")

    # 이벤트 타입을 JSON 형식으로 인코딩
    event_data = {"event_type": event_type}
    if group_by:
        event_data['group_by'] = group_by

    # URL 인코딩
    params = {
        'e': json.dumps(event_data, ensure_ascii=False),
        'start': start_date,
        'end': end_date,
        'i': i,
        'm': m
    }
    url_params = urlencode(params)

    # API URL
    url = f"https://amplitude.com/api/2/events/segmentation?{url_params}"

    headers={"Authorization": f"Basic {credentials}"}

    try:
        response = requests.get(url, headers=headers, timeout=5)

    except requests.exceptions.Timeout:
        print("The request timed out.")
    print(f"Sending request to {url} with headers {headers}")

    # 응답 처리
    if response.status_code == 200:
        return response.json()

    return f"Failed: {response.status_code}, {response.text}"

def fetch_retention(se, re, start_date, end_date):
    api_key = os.environ.get('AMPLITUDE_API_KEY')
    secret_key = os.environ.get('AMPLITUDE_SECRET_KEY')
    credentials = base64.b64encode(f"{api_key}:{secret_key}".encode("utf-8")).decode("utf-8")

    se = {"event_type": se}
    re = {"event_type": re}

    params = {
        'se': json.dumps(se, ensure_ascii=False),
        're': json.dumps(re, ensure_ascii=False),
        'start': start_date,
        'end': end_date,
        'i': 7
    }

    url_params = urlencode(params)
    url = f"https://amplitude.com/api/2/retention?{url_params}"

    headers = {"Authorization": f"Basic {credentials}"}
    print(url)
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.Timeout:
        print("요청이 시간 초과되었습니다.")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        return f"실패: {response.status_code}, {response.text}"


def fetch_all():
    api_key = os.environ.get('AMPLITUDE_API_KEY')
    secret_key = os.environ.get('AMPLITUDE_SECRET_KEY')
    credentials = base64.b64encode(f"{api_key}:{secret_key}".encode("utf-8")).decode("utf-8")

    url = f"https://amplitude.com/api/2/taxonomy/event"

    headers = {"Authorization": f"Basic {credentials}"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.Timeout:
        print("요청이 시간 초과되었습니다.")
        return None

    if response.status_code == 200:
        json_data = response.json()
        event_types = [event['event_type'] for event in json_data['data']]
        return event_types
    else:
        return f"실패: {response.status_code}, {response.text}"


event_list = fetch_all()
retention_data = {}  # 리텐션 데이터를 저장할 딕셔너리

# 모든 이벤트에 대해 리텐션 데이터를 가져옴
for event in event_list:
    retention = fetch_retention(event, "_active", '20230701', '20231016')
    retention_data[event] = retention  # 리텐션 데이터 저장
    with open(f'retention_data_{event}_20230901_20230930.json', 'w') as jsonfile:
        json.dump(retention_data, jsonfile)
