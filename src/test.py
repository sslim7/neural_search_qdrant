from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer

# Qdrant 클라이언트 초기화
client = QdrantClient(url="http://localhost:6333")

# SentenceTransformer 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 기존 컬렉션 데이터 로드
collection_name = "swit_help"
point_id = 0

# 포인트 데이터 가져오기
try:
    point_data = client.retrieve(collection_name=collection_name, ids=[point_id])
    print("Point data:", point_data)
except Exception as e:
    print("Error fetching point data:", e)

# 데이터 업데이트
if point_data:
    print("\nid:", point_data[0].id)
    print("\ncontent:", point_data[0].payload["content"])

    new_vector = model.encode(point_data[0].payload["content"]).tolist()
    # updated_point = models.PointStruct(
    #     id=point_data[0].id,
    #     vector={"default": new_vector},  # 벡터 이름 "default" 사용
    #     payload=point_data[0].payload
    # )
    #
    # # 벡터 업데이트
    # update_result = client.upsert(
    #     collection_name=collection_name,
    #     points=[updated_point]
    # )
    # print("Update result:", update_result)
    # print("\n vector:\n",new_vector)

    payload = point_data[0].payload  # 실제 payload를 사용하세요

    client.upsert(
        collection_name="swit_help",
        points=[
            models.PointStruct(
                id=point_id,
                vector={"default": new_vector},
                payload=payload
            )
        ]
    )

# 벡터 설정 확인
collection_info = client.get_collection(collection_name=collection_name)
vector_config = collection_info.config.params.vectors
print("Vector Config:", vector_config)


