from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient(":memory:")
try:
    collection_info = client.get_collection(collection_name="test_collection")
except ValueError:
    client.recreate_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=1536, distance=Distance.DOT),
    )
