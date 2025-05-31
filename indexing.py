from qdrant_utils import client
from qdrant_client.http.models import PayloadSchemaType

def create_id_index(collection_name="gromo_leads"):
    client.create_payload_index(
        collection_name=collection_name,
        field_name="_id",
        field_schema=PayloadSchemaType.KEYWORD  # or UUID if you're storing as UUID type
    )
    print("✅ Created index on '_id' field in Qdrant.")

# Run this only once:
if __name__ == "__main__":
    create_id_index()
