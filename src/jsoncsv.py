import json
import pandas as pd

# NDJSON 파일 로드
data_path = '../data/startups_demo.json'
data = []
with open(data_path, 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

# 데이터 프레임 생성
df = pd.DataFrame(data)

# CSV 파일로 저장
df.to_csv('../data/startups_demo.csv', index=False)