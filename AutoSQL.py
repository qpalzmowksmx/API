import logging
import os
import pyodbc
import time

# 필요한 함수 정의 (예시)
def fetch_flight_data():
    # 실제 API 호출 로직을 구현하세요
    pass

def store_flight_data(conn, data):
    # 실제 데이터 저장 로직을 구현하세요
    pass

def main():
    # 로깅 설정
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 환경 변수에서 데이터베이스 비밀번호 가져오기
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    if not DB_PASSWORD:
        logging.error("데이터베이스 비밀번호가 설정되지 않았습니다.")
        print("데이터베이스 비밀번호가 설정되지 않았습니다.")
        return

    # 환경 변수에서 데이터베이스 사용자명 및 다른 정보 가져오기
    DB_SERVER = os.getenv('DB_SERVER', 'localhost,1433')   # 기본값: localhost,1433
    DB_NAME = os.getenv('DB_NAME', 'TestDB')               # 실제 데이터베이스 이름으로 변경
    DB_USER = os.getenv('DB_USER', 'SA')                   # 실제 데이터베이스 사용자 이름으로 변경

    # 환경 변수 출력 (디버깅용, 보안상 주의 필요)
    logging.debug(f"DB_SERVER: {DB_SERVER}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}")
    
    # 데이터베이스 연결 설정
    try:
        connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'UID={DB_USER};'
            f'PWD={DB_PASSWORD};'
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=5;"
        )
        logging.debug(f"연결 문자열: DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={DB_SERVER}; DATABASE={DB_NAME}; UID={DB_USER}; PWD={'*' * len(DB_PASSWORD)}; Encrypt=no; TrustServerCertificate=yes; Connection Timeout=5;")
        conn = pyodbc.connect(connection_string)
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