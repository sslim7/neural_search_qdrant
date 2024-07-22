import json
import os
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

# Qdrant 클라이언트 초기화
client = QdrantClient(url="http://localhost:6333")
cnt = 0

# 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 기존 컬렉션 데이터 로드
all_points = []
scroll_result = client.scroll(collection_name="swit_help", limit=100)

while scroll_result[0]:
    all_points.extend(scroll_result[0])
    if scroll_result[1] is None:
        break
    scroll_result = client.scroll(collection_name="swit_help", limit=100, offset=scroll_result[1])

# 데이터 업데이트
updated_points = []
for point in all_points:
    if point.vector is None:
        new_vector = model.encode(point.payload["content"]).tolist()
        cnt += 1
        print(f"Updating point id={point.id} with new vector.")
        updated_points.append(
            models.PointStruct(
                id=point.id,
                vector=new_vector,
                payload=point.payload
            )
        )

# 데이터 업로드
update_result = client.upsert(
    collection_name="swit_help",
    points=updated_points
)

print(f"업데이트 완료: {cnt} 건\n", update_result)

# 업데이트된 벡터 검증
for point in updated_points:
    retrieved_points = client.retrieve(
        collection_name="swit_help",
        ids=[point.id]
    )
    print(f"Updated point id={point.id} data:", retrieved_points)