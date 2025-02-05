import logging
import os
import pyodbc

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_connection():
    DB_SERVER = os.getenv('DB_SERVER', 'localhost,1433')
    DB_NAME = os.getenv('DB_NAME', 'sql1')
    DB_USER = os.getenv('DB_USER', 'SA')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    if not DB_PASSWORD:
        logging.error("데이터베이스 비밀번호가 설정되지 않았습니다.")
        return

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
    
    try:
        conn = pyodbc.connect(connection_string)
        logging.info("MSSQL에 성공적으로 연결되었습니다.")
        conn.close()
    except pyodbc.Error as err:
        logging.error(f"MSSQL 연결 에러: {err}")

if __name__ == "__main__":
    test_connection()