from datetime import datetime, date, timedelta
from tracking_slack import send_slack_message_with_payload
import requests
import json
import os

NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("BBANGMAP_NOTION_DATABASE_KEY")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    filter_criteria = {
        "property": "파트",
        "select": {
            "does_not_equal": "기획"
        }
    }

    payload = {
        "page_size": page_size,
        "filter": filter_criteria
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print(response.status_code)

    try:
        results = data["results"]
    except KeyError:
        print("Unexpected response:", data)

    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

def main():
    today = datetime.now().date()
    tomorrow_date = today + timedelta(days=1)

    pages = get_pages()
    filtered_pages = []
    filtered_data = []
    tasks_ending_tomorrow = []

    for page in pages:
        properties = page.get("properties", {})
        if properties is None:
            continue

        due_date = properties.get("Due", {}).get("date", {})
        if due_date is None:
            continue

        start_date_str = due_date.get("start")
        end_date_str = due_date.get("end")

        if start_date_str and end_date_str:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)

            if start_date.date() <= today and end_date.date() >= today:
                filtered_pages.append(page)

    for page in filtered_pages:
        try:
            properties = page.get('properties', {})
            part_data = properties.get('파트', {}).get('select', {})
            part = part_data.get('name', '')

            name = properties.get('Name', {}).get('title', [{}])[0].get('plain_text', '')
            person_data = properties.get('담당자', {}).get('people', [{}])[0]
            person = person_data.get('name', '')
            url = page.get('url', '')
            due_data = properties.get('Due', {}).get('date', {})
            start_date = due_data.get('start', '')
            end_date = due_data.get('end', '')

            filtered_data.append({
                                 'Name': name,
                                 '담당자 이름': person,
                                 '카드 링크': url,
                                 'Start Date': start_date,
                                 'End Date': end_date
                                 })
        except Exception as e:
            continue

    for task in filtered_data:
        end_date_str = task.get('End Date', '')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if end_date == today or end_date == tomorrow_date:  # 이 부분을 수정
                tasks_ending_tomorrow.append(task)


    payload = {
        'text': '내일 끝나는 작업 목록',
        'channel': '#0-작업-순서-공유',
        'username': '작업 알리미',
        'icon_emoji': ':slack:',
        'attachments': []
    }
    if not tasks_ending_tomorrow:
        attachment = {
            'color': '#ffffff',
            'title': "오늘은 없습니다",
            'fields': []
        }
        payload['attachments'].append(attachment)
    else:
        for task in tasks_ending_tomorrow:
            attachment = {
                'color': '#36a64f',
                'title': task['Name'],
                'fields': [
                    {'title': '담당자', 'value': task['담당자 이름'], 'short': True},
                    {'title': '카드 링크', 'value': task['카드 링크'], 'short': True},
                    {'title': '시작일', 'value': task['Start Date'], 'short': True},
                    {'title': '종료일', 'value': task['End Date'], 'short': True},
                ]
            }
            payload['attachments'].append(attachment)

    send_slack_message_with_payload(payload)


if __name__ == "__main__":
    main()

