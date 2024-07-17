from datetime import datetime

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
import json

print("connect QdrantClient -", datetime.now())

client = QdrantClient(url='http://localhost:6333')

collection_name = "startups"
vector_size = 384
distance_metric = Distance.COSINE

print("create collection -", datetime.now())
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_size, distance=distance_metric),
)

fd = open("../data/startups_demo.json")

# payload is now an iterator over startup data
payload = map(json.loads, fd)

# Load all vectors into memory, numpy array works as iterable for itself.
# Other option would be to use Mmap, if you don't want to load all data into RAM
vectors = np.load("../data/startup_vectors.npy")

print("upload data to Qdrant -", datetime.now())
client.upload_collection(
    collection_name=collection_name,
    vectors=vectors,
    payload=payload,
    ids=None,  # Vector ids will be assigned automatically
    batch_size=256,  # How many vectors will be uploaded in a single request?
)
print("Finished All !!! -", datetime.now())