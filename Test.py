import os
import logging
import pyodbc

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug(f"DB_PASSWORD: {'설정됨' if "AKJ1passwd" else '설정되지 않음'}")

def test_connection():
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_USER = os.getenv('DB_USER')
    DB_NAME = os.getenv('DB_NAME')
    DB_SERVER = os.getenv("DB_SERVER")
    
    if not all([DB_PASSWORD, DB_USER, DB_NAME, DB_SERVER]):
        logging.error("필요한 환경 변수가 설정되지 않았습니다.")
        print("필요한 환경 변수가 설정되지 않았습니다.")
        return
    
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'UID={DB_USER};'
            f'PWD={DB_PASSWORD}'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        logging.info(f"연결 테스트 성공: {row[0]}")
    except pyodbc.Error as e:
        logging.error(f"연결 테스트 실패: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    test_connection()