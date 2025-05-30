from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import os
import uuid
from embedding_utils import get_openai_embedding

# Load environment variables
load_dotenv()

# Qdrant client initialization
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "gromo_leads"
VECTOR_SIZE = 1536

def ensure_collection_exists(name=COLLECTION_NAME):
    collections = client.get_collections().collections
    if name not in [col.name for col in collections]:
        print(f"🆕 Creating collection '{name}'...")
        client.recreate_collection(
            collection_name=name,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )
        ensure_payload_indexes(name)

def ensure_payload_indexes(collection=COLLECTION_NAME):
    """
    Ensure proper indexes exist for filterable fields.
    """
    try:
        client.create_payload_index(
            collection_name=collection,
            field_name="interest.products",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        print(f"✅ Payload indexes created for '{collection}'")
    except Exception as e:
        print(f"⚠️ Index creation warning: {e}")

def upsert_lead(text, metadata: dict, id: str = None, vector: list = None, collection=COLLECTION_NAME):
    """
    Upsert a lead into Qdrant. ID must be a UUID string or valid point ID.
    """
    ensure_collection_exists(collection)

    if not vector:
        vector = get_openai_embedding(text)
    if not id:
        id = str(uuid.uuid4())

    client.upsert(
        collection_name=collection,
        points=[
            models.PointStruct(
                id=id,
                vector=vector,
                payload=metadata
            )
        ]
    )
    print(f"✅ Lead with ID '{id}' upserted to Qdrant")
    return id

def search_similar(query_text, limit=5, collection=COLLECTION_NAME):
    """
    Semantic search without filters (used for audio-based input).
    """
    ensure_collection_exists(collection)
    vector = get_openai_embedding(query_text)
    results = client.search(
        collection_name=collection,
        query_vector=vector,
        limit=limit,
        with_payload=True
    )
    return results

def list_collections():
    return client.get_collections()
