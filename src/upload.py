import os
import json
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

print("connect QdrantClient -", datetime.now())

client = QdrantClient(url='http://localhost:6333')

collection_name = "swit_help"
vector_size = 384
distance_metric = Distance.COSINE
vector_name = "default"  # 벡터 이름 설정

print("create collection -", datetime.now())
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config={vector_name: VectorParams(size=vector_size, distance=distance_metric)},
)

# 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 데이터 로드
data_dir = os.path.join("..", "data")
with open(os.path.join(data_dir, "swit_help_center_ko.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# 벡터 및 payload 준비
points = []

for i, entry in enumerate(data):
    vector = model.encode(entry["content"]).tolist()
    point = {
        "id": i,
        "vector": {vector_name: vector},  # 벡터 이름을 포함하여 벡터 설정
        "payload": {
            "url": entry["url"],
            "content": entry["content"]
        }
    }
    points.append(point)

print("upload data to Qdrant -", datetime.now())
client.upsert(
    collection_name=collection_name,
    points=points,
)
print("Finished All !!! -", datetime.now())