import logging
import os

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 환경 변수 설정 (실제 사용 시 환경 변수에서 값을 가져옵니다)
os.environ['DB_SERVER'] = '127.0.0.1:1433'     # 예시 값, 실제로는 미리 설정되어 있어야 함
os.environ['DB_NAME'] = 'sql1'
os.environ['DB_USER'] = 'SA'
os.environ['DB_PASSWORD'] = 'AKJ1passwd'       # 보안상 필요에 따라 마스킹해야 함

# 환경 변수 가져오기
db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# 환경 변수 출력 (디버깅용, 보안상 주의 필요)
logging.debug(f"DB_SERVER: {db_server}, DB_NAME: {db_name}, DB_USER: {db_user}")