from collections import defaultdict
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, SearchRequest
from sentence_transformers import SentenceTransformer


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        self.qdrant_client = QdrantClient("http://localhost:6333")

    def search(self, text: str, skip: int = 0, limit: int = 5):
        vector = self.model.encode(text).tolist()

        # 실제 데이터를 가져오기 위한 호출
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            offset=skip
        )
        payloads = [hit.payload for hit in search_result]

        # 전체 문서 수를 계산하기 위한 스크롤
        scroll_result = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            limit=100
        )
        total_count = len(scroll_result.points)
        while scroll_result.next_page_offset is not None:
            scroll_result = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=scroll_result.next_page_offset
            )
            total_count += len(scroll_result.points)

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

    def col_struct(self):
        sample_data = self.qdrant_client.scroll(
            collection_name=self.collection_name,
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
        cn='swit_help'
        # 실제 데이터를 가져오기 위한 호출
        search_result = self.qdrant_client.search(
            collection_name=cn,
            query_vector=vector,
            limit=limit,
            offset=skip
        )
        payloads = [hit.payload for hit in search_result]

        # 전체 문서 수를 계산하기 위한 스크롤
        scroll_result = self.qdrant_client.scroll(
            collection_name=cn,
            limit=100
        )
        total_count = len(scroll_result.points)
        while scroll_result.next_page_offset is not None:
            scroll_result = self.qdrant_client.scroll(
                collection_name=cn,
                limit=100,
                offset=scroll_result.next_page_offset
            )
            total_count += len(scroll_result.points)

        return {"total_count": total_count, "results": payloads}