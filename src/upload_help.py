import os
import json
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from datetime import datetime

# Qdrant 클라이언트 초기화
client = QdrantClient(url="http://localhost:6333")

collection_name = "swit_help"
vector_size = 384
distance_metric = Distance.COSINE

print("connect QdrantClient -", datetime.now())

# 컬렉션 존재 여부 확인 후 삭제 및 생성
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config={"default": VectorParams(size=vector_size, distance=distance_metric)}
)

# 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 데이터 로드
data_dir = os.path.join("..", "data")
with open(os.path.join(data_dir, "swit_help_center_ko.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

points = []

for i, entry in enumerate(data):
    vector = model.encode(entry["content"]).tolist()
    point = PointStruct(
        id=i,
        vector={"default": vector},
        payload={
            "url": entry["url"],
            "content": entry["content"]
        }
    )
    points.append(point)

# 데이터 업로드
client.upsert(
    collection_name=collection_name,
    points=points
)

print("Finished All !!! -", datetime.now())