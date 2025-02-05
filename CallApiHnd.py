import requests
import json
from datetime import datetime


API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'

url = "https://fr24api.flightradar24.com/api/historic/flight-positions/full"

headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': f'Bearer {API_TOKEN}'
}
# 날짜 타임스탭프 일반 기준을 초기준으로 변환
desired_date = datetime(2025, 2, 3)
timestmap = int(desired_date.timestamp())

params = {
    'bounds': '36.160,35.160,140.140,138.140',  # 하네다 주변 좌표
    'timestamp': str(timestmap) # 25년 2월 1일
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")
