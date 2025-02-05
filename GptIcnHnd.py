import requests
import json
from datetime import datetime, timezone

# API 키 설정 (보안을 위해 환경 변수 사용 권장)
API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'

# API 엔드포인트 설정 (예: 과거 항공편 검색 엔드포인트)
# 존재하지 않는 url임임
url = "https://api.flightradar24.com/common/v1/data.json"

# 요청 헤더 설정
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# 검색할 날짜 및 시간 범위 설정 (예시: 2023년 10월 1일 00:00:00 UTC ~ 2023년 10월 2일 00:00:00 UTC)
start_date = datetime(2023, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
end_date = datetime(2023, 10, 2, 0, 0, 0, tzinfo=timezone.utc)
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# 파라미터 구성
params = {
    'airports': 'RKSI,RJTT',       # 출발지와 도착지 공항 코드 (콤마로 구분)
    'start': start_timestamp,      # 검색 시작 타임스탬프
    'end': end_timestamp,          # 검색 종료 타임스탬프
    'limit': 1000                   # 반환할 항공편 수 제한
}

try:
    # API 요청 보내기
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    # 항공편 데이터 추출
    flights = data.get('result', {}).get('response', {}).get('data', {}).get('flights', [])

    # 인천-하네다 간 항공편 필터링
    incheon_to_haneda = [flight for flight in flights if flight.get('origin', {}).get('code') == 'RKSI' and flight.get('destination', {}).get('code') == 'RJTT']

    # 결과 출력
    print(f"=== 인천공항(RKSI)에서 하네다공항(RJTT)으로 출발한 항공편 ===")
    for flight in incheon_to_haneda:
        print(json.dumps(flight, indent=4))

    print(f"\n총 항공편 수: {len(incheon_to_haneda)}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP 오류 발생: {http_err}")
    print("응답 내용:", response.text)
except Exception as err:
    print(f"오류 발생: {err}")