from collections import defaultdict
from qdrant_client import QdrantClient,models
from qdrant_client.http.models import Filter, FieldCondition, SearchRequest, models, SearchParams
from sentence_transformers import SentenceTransformer


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        self.qdrant_client = QdrantClient("http://localhost:6333")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, text: str, skip: int = 0, limit: int = 5, hnsw_ef: int = 50, score_threshold: float = 0.5):
        vector = self.model.encode(text).tolist()
        print("\nvector:\n", vector)

        # Search parameters 설정
        search_params = models.SearchParams(hnsw_ef=hnsw_ef, exact=False)

        # 실제 데이터를 가져오기 위한 호출
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=models.NamedVector(
                name="default",
                vector=vector
            ),
            search_params=search_params,
            limit=limit,
            offset=skip,
            with_vectors=True,
            score_threshold=score_threshold
        )
        payloads = [hit.payload for hit in search_result]

        # 검색 결과를 출력하여 확인
        print("\nSearch Results:")
        for i, result in enumerate(search_result):
            print(f"Result {i + 1}: ID={result.id}, Score={result.score}, Payload={result.payload}")

        # 전체 검색 결과 수 계산
        total_count = 0
        offset = 0

        while True:
            scroll_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=models.NamedVector(
                    name="default",
                    vector=vector
                ),
                search_params=search_params,
                limit=100,
                offset=offset,
                with_vectors=True,
                score_threshold=score_threshold
            )
            total_count += len(scroll_result)
            if len(scroll_result) < 100:
                break
            offset += 100

        return {"total_count": total_count, "results": payloads}

    def search_with_filter(self, text: str, city: str):
        try:
            vector = self.model.encode(text).tolist()

            city_filter = Filter(must=[FieldCondition(
                key="city",
                match={"value": city}
            )])

            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter=city_filter,
                limit=5
            )
            payloads = [hit.payload for hit in search_result]
            return payloads
        except Exception as e:
            print(f"Error in search_with_filter: {str(e)}")
            raise

    def list_collections(self):
        collections = self.qdrant_client.get_collections()
        return collections

    def col_struct(self, text: str):
        sample_data = self.qdrant_client.scroll(
            collection_name=text,
            limit=5
        )
        return sample_data

    def count_by_city(self, text: str):
        vector = self.model.encode(text).tolist()

        city_counts = defaultdict(int)

        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=100
        )

        for hit in search_result:
            if 'city' in hit.payload:
                city = hit.payload['city']
                city_counts[city] += 1

        return city_counts

    def count_all(self):
        try:
            total_count = self.qdrant_client.count(
                collection_name=self.collection_name,
                exact=True
            ).count
            return total_count
        except Exception as e:
            print(f"Error in count_all: {str(e)}")
            raise

    def search_help(self, text: str, skip: int = 0, limit: int = 5):
        vector = self.model.encode(text).tolist()
        cn = 'swit_help'

        # 실제 데이터를 가져오기 위한 호출
        search_result = self.qdrant_client.search(
            collection_name=cn,
            query_vector=vector,
            limit=limit,
            offset=skip
        )
        payloads = [hit.payload for hit in search_result]

        # 전체 문서 수를 계산하기 위한 필터 설정
        # count_filter = models.Filter(
        #     must=[
        #         models.FieldCondition(
        #             key="_vector",
        #             match=models.MatchValue(value=vector)
        #         )
        #     ]
        # )
        #
        # # 전체 문서 수 계산
        # count_result = self.qdrant_client.count(
        #     collection_name=cn,
        #     filter=count_filter,
        #     exact=True
        # )
        total_count = 0

        return {"total_count": total_count, "results": payloads}
