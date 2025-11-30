from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from .config import settings

qdrant_client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port
)


def initialize_collections():
    """Create 3 collections: code_graphs, import_files, learnings"""
    collections = ["code_graphs", "import_files", "learnings"]

    for collection in collections:
        if not qdrant_client.collection_exists(collection):
            qdrant_client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(
                    size=settings.embedding_dimension,
                    distance=Distance.COSINE
                ),
            )
            print(f"Created collection: {collection}")
        else:
            print(f"Collection already exists: {collection}")