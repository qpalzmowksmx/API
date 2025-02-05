import requests
import json
from datetime import datetime, timezone

API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'  # 보안에 유의하세요.

url = "https://fr24api.flightradar24.com/api/historic/flight-positions/full"

headers = {
    'Accept': 'application/json',
    'Accept-Version': 'v1',
    'Authorization': f'Bearer {API_TOKEN}'
}

# 원하는 날짜와 시간 설정 (2025년 1월 15일 00:00:00 UTC)
desired_date = datetime(2025, 2, 4, 0, 0, 0, tzinfo=timezone.utc)
timestamp = int(desired_date.timestamp())

# 공항과 방향 지정
airports = 'RJTT'  # 필요한 공항과 방향을 추가

params = {
    'airports': airports,  # 공항과 방향 지정
    'timestamp': str(timestamp)  # UNIX 타임스탬프
}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print("응답 내용:", response.text)
except Exception as err:
    print(f"An error occurred: {err}")