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
desired_date = datetime(2025, 1, 15, 0, 0, 0, tzinfo=timezone.utc)
timestamp = int(desired_date.timestamp())

# 공항과 방향 지정 (ICAO 코드 일관성 유지)
airports = 'inbound:RKSI,outbound:RJTT'

params = {
    'airports': airports,       # 공항과 방향 지정
    'timestamp': str(timestamp) # UNIX 타임스탬프
}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    # 입항 항공편과 출항 항공편을 분류
    inbound_flights = []
    outbound_flights = []

    if 'flights' in data and data['flights']:
        for flight in data['flights']:
            # 입항 항공편: dest_icao가 RKSI
            if flight.get('dest_icao') == 'RKSI':
                inbound_flights.append(flight)
            # 출항 항공편: orig_icao가 RJTT
            elif flight.get('orig_icao') == 'RJTT':
                outbound_flights.append(flight)

    # 입항 항공편 출력
    print("=== 인천공항(RKSI)으로 입항하는 항공편 ===")
    for flight in inbound_flights:
        print(json.dumps(flight, indent=4))

    # 출항 항공편 출력
    print("\n=== 하네다공항(RJTT)에서 출발하는 항공편 ===")
    for flight in outbound_flights:
        print(json.dumps(flight, indent=4))

    # 항공편 수 출력
    print(f"\n총 입항 항공편: {len(inbound_flights)}")
    print(f"총 출항 항공편: {len(outbound_flights)}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print("응답 내용:", response.text)
except Exception as err:
    print(f"An error occurred: {err}")