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