import requests # HTTP 요청을 위해 필요
import json # JSON 처리를 위해 필요
import os # 파일 경로 설정을 위해 필요
from datetime import datetime, timedelta, timezone # 날짜 및 시간 관련 모듈
import time # 대기시간용
import pandas as pd  # CSV 변환을 위해 필요
import logging  # 로깅을 위해 필요

# 로그 설정
logging.basicConfig(
    filename=os.path.join(r'D:\FlightData', 'api_requests.log'),  # 로그 파일 경로 설정
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 함수 정의: JSON을 CSV로 변환
def convert_json_to_csv(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # JSON 데이터를 pandas DataFrame으로 변환
        df = pd.json_normalize(data)
        
        # CSV 파일로 저장
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        
        print(f"CSV 데이터가 {csv_file_path}에 저장되었습니다.")
        logging.info(f"CSV 데이터가 {csv_file_path}에 저장되었습니다.")
    except Exception as e:
        print(f"JSON을 CSV로 변환하는 중 오류 발생: {e}")
        logging.error(f"JSON을 CSV로 변환하는 중 오류 발생: {e}")

# 환경 변수로부터 API 토큰 불러오기
API_TOKEN = os.getenv('FR24_API_TOKEN')
if not API_TOKEN:
    print("API 토큰이 환경 변수에 설정되지 않았습니다.")
    logging.error("API 토큰이 환경 변수에 설정되지 않았습니다.")
    exit()

# API 토큰 및 기본 URL 및 엔드포인트 정의
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/api/historic/flight-positions/full' # 과거 데이터 다 긁어오기

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
    'bounds': '33.300,42.300,125.800,142.800'  # Korea_IncheonAirport coordinates
}

# 저장할 디렉토리 경로 설정 (디렉토리 경로로 수정)
save_directory = r'D:\FlightData'  # 실제 디렉토리 경로로 변경하세요

# 디렉토리가 존재하지 않으면 알림 및 종료
if not os.path.exists(save_directory):
    print(f"디렉토리가 존재하지 않습니다: {save_directory}")
    logging.error(f"디렉토리가 존재하지 않습니다: {save_directory}")
    exit()

# 전체 요청 횟수 및 요청 간격 설정
total_requests = 3  # 총 20번 요청
interval_hours = 1   # 각 요청 사이의 시간 간격 (시간 단위)
time_sleep_seconds = 20  # 각 요청 사이의 대기 시간 (20 초 단위)

# 시작 타임스탬프 설정 (2025-01-01 00:00:00 UTC)
start_time_str = '2025-01-15 00:00:00'
start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

for i in range(1, total_requests + 1):
    try:
        # 타임스탬프 계산 (설정된 간격으로 증가)
        current_time = start_time + timedelta(hours=(i - 1) * interval_hours)
        current_timestamp = int(current_time)
        
        # API 파라미터에 타임스탬프 추가 (API가 지원할 경우)
        current_params = params.copy()
        # 만약 API가 'timestamp' 파라미터를 지원한다면 아래 라인 활성화
        # current_params['timestamp'] = current_timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        
        # API 요청 보내기
        response = requests.get(url, headers=headers, params=current_params)
        
        # 응답 처리
        if response.status_code == 200:
            data = response.json()
            print(f"Request {i}: Success - Timestamp: {current_timestamp}")
            logging.info(f"Request {i}: Success - Timestamp: {current_timestamp}")
            
            # 파일명에 숫자 추가 (예: output1.json, output2.json, ...)
            file_name = f"output{i}.json"
            file_path = os.path.join(save_directory, file_name)
            
            # JSON 데이터를 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            
            print(f"JSON 데이터가 {file_path}에 저장되었습니다.")
            logging.info(f"JSON 데이터가 {file_path}에 저장되었습니다.")
            
            # JSON을 CSV로 변환
            csv_file_name = f"output{i}.csv"
            csv_file_path = os.path.join(save_directory, csv_file_name)
            convert_json_to_csv(file_path, csv_file_path)
        else:
            print(f"Request {i} Error: {response.status_code}")
            print(response.text)
            logging.error(f"Request {i} Error: {response.status_code} - {response.text}")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Request {i} HTTP error occurred: {http_err}")
        logging.error(f"Request {i} HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request {i} Request exception: {req_err}")
        logging.error(f"Request {i} Request exception: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Request {i} JSON decode error: {json_err}")
        logging.error(f"Request {i} JSON decode error: {json_err}")
    except Exception as err:
        print(f"Request {i} Unexpected error: {err}")
        logging.error(f"Request {i} Unexpected error: {err}")
    
    # 요청 간 대기 시간 설정 (20초 대기)

   time.sleep(time_sleep_seconds)  # 20초 대기