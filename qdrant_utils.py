from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def create_collection(name="gromo_leads"):
    client.recreate_collection(
        collection_name=name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
    )

def upsert_lead(text, metadata: dict, collection="gromo_leads", id=None, vector=None):
    from embedding_utils import get_openai_embedding
    if not vector:
        vector = get_openai_embedding(text)
    if not id:
        id = str(uuid.uuid4())
    client.upsert(
        collection_name=collection,
        points=[
            models.PointStruct(id=id, vector=vector, payload=metadata)
        ]
    )
    return id

def list_collections():
    return client.get_collections()

def search_similar(query_text, collection="gromo_leads", limit=5):
    from embedding_utils import get_openai_embedding
    query_vector = get_openai_embedding(query_text)
    results = client.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=limit,
        with_payload=True
    )
    return results

def ensure_payload_indexes(collection="gromo_leads"):
    client.create_payload_index(
        collection_name=collection,
        field_name="contact.preferred_language",
        field_schema=models.PayloadSchemaType.KEYWORD
    )
    client.create_payload_index(
        collection_name=collection,
        field_name="interest.products",
        field_schema=models.PayloadSchemaType.KEYWORD
    )

