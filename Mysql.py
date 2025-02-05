from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 연결 (파일 기반)
DATABASE_URL = 'sqlite:///flights.db'

# 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# 베이스 클래스 생성
Base = declarative_base()

# Flights 테이블 모델 정의
class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    callsign = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float)
    altitude = Column(Float)
    timestamp = Column(DateTime, nullable=False)
    registration = Column(String)  # 비행기 등록번호
    aircraft_type = Column(String)  # 항공기 유형

    def __repr__(self):
        return f"<Flight(id={self.id}, callsign='{self.callsign}', origin='{self.origin}', destination='{self.destination}')>"

# 테이블 생성
Base.metadata.create_all(engine)