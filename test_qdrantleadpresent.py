# test_qdrant_lead_presence.py

from qdrant_utils import client
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import sys

def check_lead_in_qdrant(lead_id: str, collection="gromo_leads"):
    try:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="_id",
                    match=MatchValue(value=lead_id)
                )
            ]
        )

        result = client.search(
            collection_name=collection,
            query_vector=[0.0] * 1536,  # dummy vector, only filter will be used
            query_filter=query_filter,
            limit=1,
            with_payload=True
        )

        if not result:
            print(f"❌ Lead with ID {lead_id} not found in Qdrant.")
        else:
            print(f"✅ Lead found in Qdrant. Full payload:\n")
            for point in result:
                print(point.payload)

    except Exception as e:
        print(f"⚠️ Error checking Qdrant: {e}")

if __name__ == "__main__":
    lead_id = "eae67dd7-cb8a-44bc-a790-e5174745ed64"
    check_lead_in_qdrant(lead_id)
