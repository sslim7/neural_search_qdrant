from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import pandas as pd
from tqdm.notebook import tqdm

# NDJSON 파일 로드
print("데이터 프레임 생성...\n","-",datetime.now())
df = pd.read_json("../data/startups_demo.json", lines=True)

# 모델 초기화
print("모델 초기화...\n",len(df),"건","-",datetime.now())
model = SentenceTransformer(
    "all-MiniLM-L6-v2", device="cpu"
)  # or device="cpu" if you don't have a GPU

# 벡터화
print("백터화...\n","-",datetime.now())
vectors = model.encode(
    [row.alt + ". " + row.description for row in df.itertuples()],
    show_progress_bar=True,
)
vectors.shape
# > (40474, 384)

# CSV 파일로 저장
print("백터 파일로 저장...\n","-",datetime.now())
np.save("../data/startup_vectors.npy", vectors, allow_pickle=False)
print("Finished in data/startup_vectors.npy","-",datetime.now())
