from amplitude_event_api import fetch_event_segmentation
from tracking_slack import send_to_slack
from datetime import datetime, timedelta

# 현재 날짜 가져오기
today = datetime.now()
# 1일 전 날짜를 계산하기
yesterday = today - timedelta(days=1)

# 날짜를 YYYYMMDD 형식으로 변환
start_date = yesterday.strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')

review_write = fetch_event_segmentation(
    event_type="REVIEW_WRITE",
    start_date=start_date,
    end_date=end_date
)

try:
    review_write_value = review_write['data']['series'][0][0]
except ValueError:
    print(f"No data available for {start_date}.")

send_to_slack(f"\n어제 리뷰 작성 갯수 : {review_write_value}")
