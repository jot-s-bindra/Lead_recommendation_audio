from mongo_utils import get_lead_by_id
from qdrant_utils import upsert_lead
from embedding_utils import get_openai_embedding

def format_lead_text(lead: dict) -> str:
    contact = lead.get("contact", {})
    interest = lead.get("interest", {})
    personal = lead.get("personal_data", {})

    summary = f"""
    Name: {contact.get('name')}, Phone: {contact.get('phone')}
    Age: {personal.get('age')}, State: {personal.get('state')}, Occupation: {personal.get('occupation')}, Income: {personal.get('income')}
    Interested in: {', '.join(interest.get('products', []))}, Interest Level: {interest.get('interest_level')}
    Notes: {lead.get('notes')}
    Summary: {lead.get('summary')}
    """
    return summary.strip()

def push_lead_to_qdrant(mongo_id: str):
    lead = get_lead_by_id(mongo_id)
    lead_text = format_lead_text(lead)
    vector = get_openai_embedding(lead_text)

    lead["_id"] = str(lead["_id"])  # already string, just to be safe

    upsert_lead(
        text=lead_text,
        metadata=lead,
        vector=vector,
        id=lead["_id"]  # UUID string
    )
    print(f"✅ Lead {lead['_id']} pushed to Qdrant.")



if __name__ == "__main__":
    test_id = input("Enter Mongo _id of the lead to insert: ")
    push_lead_to_qdrant(test_id)