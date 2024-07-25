from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

# Qdrant 클라이언트 초기화
client = QdrantClient(url="http://localhost:6333")

# SentenceTransformer 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 기존 컬렉션 데이터 로드
all_points = []
scroll_result = client.scroll(collection_name="swit_help", limit=100)

while scroll_result[0]:  # scroll_result.points 대신 scroll_result[0] 사용
    all_points.extend(scroll_result[0])
    if scroll_result[1] is None:  # scroll_result.next_page_offset 대신 scroll_result[1] 사용
        break
    scroll_result = client.scroll(collection_name="swit_help", limit=100, offset=scroll_result[1])

# 데이터 업데이트
# updated_points = []
for point in all_points:
    if point.vector is None:
        new_vector = model.encode(point.payload["content"]).tolist()
        client.update_vectors(
            collection_name="swit_help",
            points=[
                models.PointVectors(
                    id=point.id,
                    vector={"default":new_vector,},
                ),
            ],
        )
        print("\n업데이트:", point.id)
# for point in all_points:
#     if point.vector is None:
#         new_vector = model.encode(point.payload["content"]).tolist()
#         updated_point = models.PointVectors(
#             id=point.id,
#             vector=new_vector
#         )
#         updated_points.append(updated_point)
#
# # 데이터 업로드
# print(updated_points)
# update_result = client.update_vectors(
#     collection_name="swit_help",
#     points=updated_points
# )


# 업데이트된 벡터 검증
for point in all_points:
    retrieved_points = client.retrieve(
        collection_name="swit_help",
        ids=[point.id]
    )
    print(f"Updated point id={point.id} data:", retrieved_points)