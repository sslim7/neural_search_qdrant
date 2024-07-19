import json
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Qdrant 클라이언트 초기화
client = QdrantClient(url="http://localhost:6333")

# 컬렉션 생성
client.recreate_collection(
    collection_name="swit_help",
    vectors_config={"default": {"size": 384, "distance": "Cosine"}}
)

# 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 데이터 로드
with open("..\data\swit_help_center.json", "r") as f:
    data = json.load(f)

points = []

for i, entry in enumerate(data):
    vector = model.encode(entry["content"]).tolist()
    point = {
        "id": i,
        "vector": vector,
        "payload": {
            "url": entry["url"],
            "content": entry["content"]
        }
    }
    points.append(point)

# 데이터 업로드
client.upsert(
    collection_name="swit_help",
    points=points
)