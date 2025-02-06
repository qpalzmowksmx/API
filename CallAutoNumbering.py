import requests
import json
import os
from datetime import datetime, timedelta
import time # 대기시간용

# 필요한 모듈 임포트
from datetime import datetime, timedelta

# 문자열로부터 초기 타임스탬프 생성
initial_timestamp = datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

# API 토큰 및 기본 URL 및 엔드포인트 정의
API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/live/flight-positions/light'

# 완전한 URL 구성
url = f"{BASE_URL}{ENDPOINT}"

# 헤더 정의, Authorization 헤더에 API 토큰 포함
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept-Version': 'v1'
}

# 기본 쿼리 파라미터 정의
params = {
    'bounds': '33.27,41.27,122.26,130.26'  # Korea_IncheonAirport coordinates
}

# 저장할 디렉토리 경로 설정 (디렉토리 경로로 수정)
save_directory = r'D:\FlightData'  # 실제 디렉토리 경로로 변경하세요

# 디렉토리가 존재하지 않으면 알림 및 종료
if not os.path.exists(save_directory):
    print(f"디렉토리가 존재하지 않습니다: {save_directory}")
    exit()

# 전체 요청 횟수 및 요청 간격 설정
total_requests = 20  # 20번 요청
interval_hours = 1   # 각 요청 사이의 시간 간격 (시간 단위)
time.sleep(20)  # 20초 대기

for i in range(1, total_requests + 1):
    try:
        # 타임스탬프 계산 (설정된 간격으로 증가)
        current_timestamp = initial_timestamp + timedelta(hours=(i - 1) * interval_hours)
        
        # API 파라미터에 타임스탬프 추가 (API 지원 여부에 따라 조정)
        current_params = params.copy()
        # 만약 API가 'timestamp' 파라미터를 지원한다면 아래 라인 활성화
        # current_params['timestamp'] = current_timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        
        # API 요청 보내기
        response = requests.get(url, headers=headers, params=current_params)
        
        # 응답 처리
        if response.status_code == 200:
            data = response.json()
            print(f"Request {i}: Success - Timestamp: {current_timestamp}")
            
            # 파일명에 숫자 추가 (예: output1.json, output2.json, ...)
            file_name = f"output{i}.json"
            file_path = os.path.join(save_directory, file_name)
            
            # JSON 데이터를 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            
            print(f"JSON 데이터가 {file_path}에 저장되었습니다.")
        else:
            print(f"Request {i} Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Request {i} HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request {i} Request exception: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Request {i} JSON decode error: {json_err}")
    except Exception as err:
        print(f"Request {i} Unexpected error: {err}")

# 완료 메시지 출력
print("모든 요청이 완료되었습니다.")
