from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, Match, SearchRequest
from sentence_transformers import SentenceTransformer

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")

    def search(self, text: str):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=5  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads

    def search_with_filter(self, text: str, city: str):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        # Define a filter for cities
        city_filter = Filter(
            must=[FieldCondition(
                key="city",
                match=Match(value=city)  # Use Match instead of FieldMatch
            )]
        )

        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=city_filter,
            limit=5
        )
        payloads = [hit.payload for hit in search_result]
        return payloads