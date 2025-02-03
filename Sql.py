import requests
import mysql.connector
from datetime import datetime
import os
import time
import logging

# 로깅 설정
logging.basicConfig(
    filename='flight_data.log',  # 로그 파일 이름
    level=logging.INFO,           # 로그 레벨 설정 (INFO, DEBUG, ERROR 등)
    format='%(asctime)s - %(levelname)s - %(message)s'  # 로그 포맷
)

def fetch_flight_data():
    API_TOKEN = os.getenv('FR24_API_TOKEN')  # 환경 변수에서 API 토큰 가져오기
    if not API_TOKEN:
        logging.error("API 토큰이 설정되지 않았습니다.")
        print("API 토큰이 설정되지 않았습니다.")
        return None
    
    BASE_URL = 'https://fr24api.flightradar24.com/api'
    ENDPOINT = '/live/flight-positions/light'
    
    url = f"{BASE_URL}{ENDPOINT}"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}',
        'Accept-Version': 'v1'
    }
    
    params = {
        'bounds': '33.0,124.0,43.0,132.0',  # 한국 전역을 포괄하는 좌표
        'query': 'KE',                      # 대한항공의 IATA 코드 'KE'
        'limit': 100                        # 필요한 데이터 개수 조정
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP 에러 발생: {errh}")
        print(f"HTTP 에러 발생: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"연결 에러 발생: {errc}")
        print(f"연결 에러 발생: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"타임아웃 에러 발생: {errt}")
        print(f"타임아웃 에러 발생: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"요청 에러 발생: {err}")
        print(f"요청 에러 발생: {err}")
    except Exception as e:
        logging.error(f"알 수 없는 에러: {e}")
        print(f"알 수 없는 에러: {e}")
    return None

def store_flight_data(conn, data):
    cursor = conn.cursor()
    flights = data.get('flights', [])
    
    for flight in flights:
        # 호출 신호가 'KE'로 시작하는지 확인 (대한항공)
        callsign = flight.get('callsign', '')
        if not callsign.startswith('KE'):
            continue  # 대한항공 비행기가 아닌 경우 건너뜀
        
        # 필요한 데이터 추출
        flight_id = flight.get('fr24_id')
        hex_code = flight.get('hex')
        lat = flight.get('lat')
        lon = flight.get('lon')
        track = flight.get('track')
        alt = flight.get('alt')
        gspeed = flight.get('gspeed')
        vspeed = flight.get('vspeed')
        squawk = flight.get('squawk')
        timestamp_str = flight.get('timestamp')
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ") if timestamp_str else None
        source = flight.get('source')
        
        # 데이터베이스에 삽입
        insert_query = """
        INSERT INTO flights (fr24_id, hex, callsign, lat, lon, track, alt, gspeed, vspeed, squawk, timestamp, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            lat = VALUES(lat),
            lon = VALUES(lon),
            track = VALUES(track),
            alt = VALUES(alt),
            gspeed = VALUES(gspeed),
            vspeed = VALUES(vspeed),
            squawk = VALUES(squawk),
            timestamp = VALUES(timestamp),
            source = VALUES(source)
        """
        cursor.execute(insert_query, (flight_id, hex_code, callsign, lat, lon, track, alt, gspeed, vspeed, squawk, timestamp, source))
    
    conn.commit()
    cursor.close()

def main():
    # 환경 변수에서 데이터베이스 비밀번호 가져오기
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    if not DB_PASSWORD:
        logging.error("데이터베이스 비밀번호가 설정되지 않았습니다.")
        print("데이터베이스 비밀번호가 설정되지 않았습니다.")
        return
    
    # 데이터베이스 연결 설정
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="your_user",                  # 데이터베이스 사용자 이름
            password=DB_PASSWORD,              # 환경 변수로 관리
            database="your_database"           # 데이터베이스 이름
        )
    except mysql.connector.Error as err:
        logging.error(f"MySQL 연결 에러: {err}")
        print(f"MySQL 연결 에러: {err}")
        return
    
    try:
        while True:
            data = fetch_flight_data()
            if data:
                flights = data.get('flights', [])
                if not flights:
                    logging.info("비행기 데이터가 없습니다.")
                    print("비행기 데이터가 없습니다.")
                else:
                    store_flight_data(db, data)
                    logging.info("데이터가 성공적으로 저장되었습니다.")
                    print("데이터가 성공적으로 저장되었습니다.")
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
        if db.is_connected():
            db.close()
            logging.info("데이터베이스 연결이 종료되었습니다.")
            print("데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()