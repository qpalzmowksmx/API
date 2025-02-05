import requests
import json
from datetime import datetime, timezone

# API 설정
API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'
ENDPOINT = "https://fr24api.flightradar24.com/api/historic/flight-positions/full"

# 요청 헤더 설정
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept-Version': 'v1',
    'Content-Type': 'application/json'
}

# 검색할 날짜 및 시간 범위 설정
# 예시: 2023년 10월 1일 00:00:00 UTC ~ 2023년 10월 2일 00:00:00 UTC
start_date = datetime(2025, 1, 15, 0, 0, 0, tzinfo=timezone.utc)
end_date = datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# 요청 파라미터 구성
params = {
    'origin': 'RKSI',            # 인천공항 ICAO 코드
    'destination': 'RJTT',       # 하네다공항 ICAO 코드
    'start': start_timestamp,    # 검색 시작 타임스탬프
    'end': end_timestamp,        # 검색 종료 타임스탬프
    'limit': 1000                 # 반환할 항공편 수 제한 (필요에 따라 조정)
}

try:
    # API 요청 보내기
    response = requests.get(ENDPOINT, headers=headers, params=params)
    response.raise_for_status()  # 응답 상태 코드 확인
    data = response.json()

    # 항공편 데이터 추출
    flights = data.get('result', {}).get('response', {}).get('data', {}).get('flights', [])

    # 인천-하네다 간 항공편 필터링 (이미 필터링된 상태일 가능성)
    incheon_to_haneda = [flight for flight in flights if flight.get('origin', {}).get('code') == 'RKSI' and flight.get('destination', {}).get('code') == 'RJTT']

    # 결과 출력
    print("=== 인천공항(RKSI)에서 하네다공항(RJTT)으로 출발한 항공편 ===")
    for flight in incheon_to_haneda:
        print(json.dumps(flight, indent=4))

    print(f"\n총 항공편 수: {len(incheon_to_haneda)}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP 오류 발생: {http_err}")
    print("응답 내용:", response.text)
except Exception as err:
    print(f"오류 발생: {err}")