from amplitude_event_api import fetch_event_segmentation
from tracking_slack import send_to_slack
from datetime import datetime, timedelta
import json

# 현재 날짜 가져오기
today = datetime.now()
# 1일 전 날짜를 계산하기
yesterday = today - timedelta(days=7)

# 날짜를 YYYYMMDD 형식으로 변환
start_date = yesterday.strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')

search_result = fetch_event_segmentation(
    event_type="SEARCH_RESULT",
    start_date=start_date,
    end_date=end_date,
    i=7,
    m="totals",
    group_by=[{"type": "event", "value": "SEARCH_KEYWORD"}]
)


# 'series'와 'seriesLabels' 데이터를 매칭하기 위한 작업을 수행합니다.
series_data = search_result['data']['series']
series_labels = search_result['data']['seriesLabels']

# 'series'와 'seriesLabels'의 길이가 같은지 확인
if len(series_data) != len(series_labels):
    matched_data = "series와 seriesLabels의 길이가 다릅니다."
else:
    # 'series'와 'seriesLabels'를 순서대로 매칭
    matched_data = [
        {"series": series, "label": label[1]}
        for series, label in zip(series_data, series_labels)
    ]

sliced_matched_data = matched_data[:30]
for item in sliced_matched_data:
    item['sum'] = sum(item['series'])

# 'sum' 값에 따라 데이터를 정렬합니다.
sorted_data = sorted(sliced_matched_data, key=lambda x: x['sum'], reverse=True)

# 'series' 항목을 제거하고 순위를 매깁니다.
ranked_data = [{"Rank": i+1, "Label": item['label'], "Sum": item['sum']} for i, item in enumerate(sorted_data)]

# 각 순위별로 문자열을 만들고 개행 문자로 합칩니다.
ranked_string = "\n".join([f"{str(item['Rank']).zfill(2)}: {item['Label']} {item['Sum']}" for item in ranked_data])

send_to_slack(f"{end_date} 1주일간 검색 순위\n{ranked_string}")
