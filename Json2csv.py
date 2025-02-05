import json
import csv
import os

# JSON 파일 경로 설정
json_file_path = r'C:\Users\SD1-06\Documents\SqlFor\output.json'  # 실제 JSON 파일 경로로 변경
# 변환된 CSV 파일 경로 설정
csv_file_path = r'C:\Users\SD1-06\Documents\SqlFor\output.csv'    # 원하는 CSV 파일 경로로 변경

# JSON 데이터 로드
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 'data' 키의 값이 리스트인지 확인
if 'data' in data and isinstance(data['data'], list):
    records = data['data']
else:
    raise ValueError("JSON 파일의 구조가 예상과 다릅니다. 'data' 키가 존재하고 리스트여야 합니다.")

# CSV 헤더 정의 (JSON의 키와 일치해야 함)
# 첫번째 레코드에서 키를 추출하여 동적으로 헤더를 설정할 수 있습니다.
headers = records[0].keys()

# CSV 파일로 기록
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    for record in records:
        writer.writerow(record)

print(f"CSV 파일이 성공적으로 생성되었습니다: {csv_file_path}")