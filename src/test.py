from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer

# Qdrant 클라이언트 초기화
client = QdrantClient(url="http://localhost:6333")

# SentenceTransformer 모델 초기화
model = SentenceTransformer("all-MiniLM-L6-v2")

# 기존 컬렉션 데이터 로드
collection_name = "swit_help"

# 컬렉션 정보 가져오기
collection_info = client.get_collection(collection_name=collection_name)

# 컬렉션 정보를 사전으로 변환
collection_info_dict = collection_info.dict()

# 벡터 구성 정보 출력
print("Vector Config:", collection_info_dict)

point_id="0520eb8c-90df-4ed9-aef1-82914151248a"
point_data=[]
try:
    point_data = client.retrieve(collection_name=collection_name, ids=[point_id])
except Exception as e:
    print("Error fetching point data:", e)
# 데이터 업데이트
print("\nid:", point_data[0].id)
print("\ncontent:", point_data[0].payload["content"])
print("\nvector:", point_data[0].vector)

new_vector = model.encode(point_data[0].payload["content"]).tolist()
op_info = client.update_vectors(
    collection_name=collection_name,
    points=[
        models.PointVectors(
            id=point_data[0].id,
            vector=new_vector,
        ),
    ],
)
print("\nupdated_vectors~드!!.",op_info)

# op_info = client.upsert(collection_name=collection_name,
#                         points=[
#                             PointStruct(id=point_data[0].id,
#                                         vector=new_vector,
#                                         payload=point_data[0].payload),
#                             ]
#                         )
# print("\nupsert!!.",op_info)
