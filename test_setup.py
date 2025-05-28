import os
from dotenv import load_dotenv
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from qdrant_utils import client, search_similar
from embedding_utils import get_openai_embedding

load_dotenv()

def test_embedding():
    print("🔍 Testing OpenAI Embedding...")
    test_text = "Looking for a credit card for someone who speaks Hindi and lives in Noida"
    embedding = get_openai_embedding(test_text)
    assert isinstance(embedding, list) and len(embedding) == 1536
    print("✅ Embedding generation successful.")

def test_qdrant_connection():
    print("🔌 Testing Qdrant Connection...")
    collections = client.get_collections()
    assert "gromo_leads" in [col.name for col in collections.collections]
    print("✅ Qdrant connection and collection verified.")

def test_query_vector_search():
    print("📡 Running Vector Search Test...")
    query = "Need a lead from Hindi-speaking region interested in home loan"
    results = search_similar(query_text=query)
    assert results and len(results) > 0
    print(f"✅ Search returned {len(results)} leads. Top result:\n→ {results[0].payload['contact']}")

def test_payload_filtering():
    print("🧪 Testing Payload Filters...")
    query = "Home loan for Marathi-speaking user"
    vector = get_openai_embedding(query)
    filtered_results = client.search(
        collection_name="gromo_leads",
        query_vector=vector,
        limit=3,
        with_payload=True,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="contact.preferred_language",
                    match=MatchValue(value="Marathi")
                )
            ]
        )
    )
    print(f"✅ Filtered results found: {len(filtered_results)}")
    for res in filtered_results:
        print("→", res.payload["contact"])

if __name__ == "__main__":
    print("🧪 Starting setup test...")
    test_embedding()
    test_qdrant_connection()
    test_query_vector_search()
    test_payload_filtering()
    print("🎉 All checks passed.")
