import requests
from google_play_scraper import app

def fetch_app_store_reviews(app_id):
    url = f"https://itunes.apple.com/kr/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
    response = requests.get(url)
    reviews = response.json()  # 리뷰 파싱
    return reviews

def fetch_play_store_reviews(app_id):
    result = app(
        "bbangmap.com",
        lang='kr',  # 언어 설정
        country='us'  # 국가 설정
    )
    return result['comments']  # 리뷰만 추출

def check_for_new_reviews(app_store_reviews, play_store_reviews, last_checked_id):
    new_reviews = []

    for review in app_store_reviews:
        if review['id'] > last_checked_id:
            new_reviews.append(review)

    for review in play_store_reviews:
        if review['id'] > last_checked_id:
            new_reviews.append(review)

    return new_reviews

def fetch_app_store_reviews(app_id):
    try:
        url = f"https://itunes.apple.com/kr/rss/customerreviews/id=id1595032110/json"
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 확인
        reviews = response.json()
    except requests.RequestException as e:
        print(f"App Store API 에러: {e}")
        return None
    return reviews

def send_to_slack(message):
    try:
        webhook_url = "YOUR_SLACK_WEBHOOK_URL"
        payload = {"text": message}
        response = requests.post(webhook_url, json.dumps(payload))
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Slack API 에러: {e}")

app_store_reviews = fetch_app_store_reviews("1595032110")
#play_store_reviews = fetch_play_store_reviews("YOUR_PLAY_STORE_ID")

#new_reviews = check_for_new_reviews(app_store_reviews, play_store_reviews)  # 새 리뷰 찾는 로직 구현 필요

#for review in new_reviews:
#    send_to_slack(review)
print(app_store_reviews)
