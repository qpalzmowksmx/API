import requests
import json
import os
from datetime import datetime, timedelta

# 문자열로부터 초기 타임스탬프 생성
initial_timestamp = datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

# API 토큰 및 기본 URL 및 엔드포인트 정의
API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/live/flight-positions/light'

# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"

# Define the headers, including the Authorization header with your API token
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept-Version': 'v1'
}

# Define any query parameters, if needed (optional)
params = {
    'bounds': '50.682,46.218,14.422,22.243'  # Slovenia IntAirport coordinates
}

# Make the GET request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print("Live Flight Positions:")
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# 응답 상태 코드 확인
if response.status_code == 200:
    data = response.json()  # JSON 데이터 파싱

    # 저장할 디렉토리 경로 설정
    save_directory = 'D:\FlightData'  # 실제 경로 확인

    # 디렉토리가 존재하지 않으면 알림
    if not os.path.exists(save_directory):
        print(f"디렉토리가 존재하지 않습니다: {save_directory}")
        exit
        
    # 파일명 설정 (예: output.json)
    file_path = os.path.join(save_directory, 'output.json')

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"JSON 데이터가 {file_path}에 저장되었습니다.")
else:
    print(f"API 요청 실패: 상태 코드 {response.status_code}")