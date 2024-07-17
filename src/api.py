from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
client = QdrantClient(url='http://localhost:6333')

class Query(BaseModel):
    query: str

@app.post("/search")
async def search(query: Query):
    query_vector = model.encode([query.query])[0]
    results = client.search(
        collection_name="company_descriptions",
        query_vector=query_vector,
        limit=5
    )
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)