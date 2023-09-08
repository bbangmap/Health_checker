from amplitude_event_api import fetch_event_segmentation
from tracking_slack import send_to_slack
from datetime import datetime, timedelta
import os

# 현재 날짜 가져오기
today = datetime.now()
# 1일 전 날짜를 계산하기
yesterday = today - timedelta(days=1)

# 날짜를 YYYYMMDD 형식으로 변환
start_date = yesterday.strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')

all_user_result = fetch_event_segmentation(
    event_type="_all",
    start_date=start_date,
    end_date=end_date
)

new_user_result = fetch_event_segmentation(
    event_type="_new",
    start_date=start_date,
    end_date=end_date
)

try:
    new_value = new_user_result['data']['series'][0][0]
    all_value = all_user_result['data']['series'][0][0]
except ValueError:
    print(f"No data available for {start_date}.")

send_to_slack(f"{start_date}\n\nDAU : {all_value}\nNEW_USER : {new_value}")
