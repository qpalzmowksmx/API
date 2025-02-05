import re

# 파일 경로 설정
input_file = 'output.json'
output_file = 'output_fixed.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = file.read()

# 작은따옴표를 큰따옴표로 변환 (간단한 방법, 모든 경우에 맞지 않을 수 있음)
data = re.sub(r"'", '"', data)

with open(output_file, 'w', encoding='utf-8') as file:
    file.write(data)

print(f"변환된 JSON 파일이 저장되었습니다: {output_file}")