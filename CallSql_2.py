import os
import time
import logging
import pyodbc
import requests
from datetime import datetime

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

def store_flight_data(conn, data):
    """
    비행기 데이터를 MSSQL 데이터베이스에 저장하는 함수.
    테이블 이름과 컬럼을 실제 DB 구조에 맞게 변경하세요.
    """
    if not data:
        logging.info("저장할 데이터가 없습니다.")
        print("저장할 데이터가 없습니다.")
        return

    flights = data.get('flights', [])  # flights 변수 정의

    if not flights:
        logging.info("저장할 비행기 데이터가 없습니다.")
        print("저장할 비행기 데이터가 없습니다.")
        return

    try:
        cursor = conn.cursor()
        for flight in flights:    # API 응답 구조에 맞게 변경
            cursor.execute("""
                INSERT INTO Flights (
                    fr24_id, hex, callsign, lat, lon, track, alt, gspeed, vspeed, squawk, timestamp, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
                flight.get('fr24_id'),
                flight.get('hex'),
                flight.get('callsign'),
                flight.get('lat'),
                flight.get('lon'),
                flight.get('track'),
                flight.get('alt'),
                flight.get('gspeed'),
                flight.get('vspeed'),
                flight.get('squawk'),
                datetime.strptime(flight.get('timestamp'), '%Y-%m-%dT%H:%M:%SZ'),  # ISO 8601 형식 변환
                flight.get('source')
            )
            logging.debug(f"삽입된 데이터: {flight}")
        conn.commit()
        logging.info("데이터베이스에 데이터 삽입 완료.")
        logging.info(f"{len(flights)}개의 비행기 데이터가 저장되었습니다.")
        print("데이터가 성공적으로 저장되었습니다.")
    except pyodbc.Error as e:
        logging.error(f"MSSQL 데이터 삽입 오류: {e}")
        print(f"MSSQL 데이터 삽입 오류: {e}")
    finally:
        cursor.close()

def main():
    # 환경 변수에서 데이터베이스 비밀번호 가져오기
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    if not DB_PASSWORD:
        logging.error("데이터베이스 비밀번호가 설정되지 않았습니다.")
        print("데이터베이스 비밀번호가 설정되지 않았습니다.")
        return

    # 환경 변수에서 데이터베이스 사용자명 및 다른 정보 가져오기
    DB_SERVER = os.getenv('DB_SERVER', 'localhost,1433')   # 기본값: localhost,1433
    DB_NAME = os.getenv('DB_NAME', 'TestDB')           # 실제 데이터베이스 이름으로 변경
    DB_USER = os.getenv('DB_USER', 'SA')                   # 실제 데이터베이스 사용자 이름으로 변경

    # 환경 변수 출력 (디버깅용, 보안상 주의 필요)
    logging.debug(f"DB_SERVER: {DB_SERVER}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}")

    # 데이터베이스 연결 설정
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'UID={DB_USER};'
            f'PWD={DB_PASSWORD}'
        )
        logging.info("MSSQL에 성공적으로 연결되었습니다.")
        print("MSSQL에 성공적으로 연결되었습니다.")
    except pyodbc.Error as err:
        logging.error(f"MSSQL 연결 에러: {err}")
        print(f"MSSQL 연결 에러: {err}")
        return

    try:
        while True:
            data = fetch_flight_data()
            if data:
                flights = data.get('flights', [])        # API 응답 구조에 맞게 변경
                if not flights:
                    logging.info("비행기 데이터가 없습니다.")
                    print("비행기 데이터가 없습니다.")
                else:
                    store_flight_data(conn, data)
            else:
                logging.info("API 응답이 없습니다.")
                print("API 응답이 없습니다.")

            print("15초 대기 중...")
            time.sleep(15)  # 15초 대기
    except KeyboardInterrupt:
        logging.info("사용자에 의해 스크립트가 중단되었습니다.")
        print("\n스크립트가 중단되었습니다.")
    except Exception as e:
        logging.error(f"예상치 못한 에러: {e}")
        print(f"예상치 못한 에러: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("데이터베이스 연결이 종료되었습니다.")
            print("데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()
