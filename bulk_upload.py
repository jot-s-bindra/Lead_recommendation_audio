import random
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from qdrant_utils import create_collection, upsert_lead, client
from qdrant_client.http.exceptions import UnexpectedResponse
from embedding_utils import get_openai_embedding

lead_notes_path = Path("templates_db/lead.txt")
lead_notes = [line.strip() for line in lead_notes_path.read_text().splitlines() if line.strip()]

regions = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad",
           "Jaipur", "Lucknow", "Bhopal", "Chandigarh", "Nagpur", "Indore", "Patna", "Surat",
           "Noida", "Gurgaon", "Amritsar", "Ludhiana", "Thane", "Faridabad", "Ranchi", "Jalandhar"]
languages = ["Hindi", "English", "Punjabi", "Marathi", "Tamil", "Telugu", "Kannada", "Gujarati",
             "Malayalam", "Bengali", "Urdu", "Odia", "Assamese", "Konkani"]
products = ["home_loan", "credit_card", "insurance", "personal_loan", "business_loan"]
interest_levels = ["low", "medium", "high"]
urgency_levels = ["immediate", "within_week", "within_month"]
first_names = ["Rahul", "Neha", "Amit", "Priya", "Karan", "Deepika", "Ravi", "Meena", "Ankit", "Pooja"]
last_names = ["Sharma", "Verma", "Kumar", "Gupta", "Singh", "Yadav", "Mehra", "Jain", "Chopra", "Patel"]

try:
    client.get_collection("gromo_leads")
    print("📦 Collection already exists, skipping recreation.")
except UnexpectedResponse:
    create_collection()
    print("🆕 Created new collection.")

def generate_lead():
    note = random.choice(lead_notes)
    region = random.choice(regions)
    language = random.choice(languages)
    selected_products = random.sample(products, k=random.randint(1, 2))

    contact = {
        "name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "phone": f"+91{random.randint(7000000000, 9999999999)}",
        "email": f"user{random.randint(1000,9999)}@example.com",
        "age": random.randint(22, 60),
        "region": region,
        "preferred_language": language
    }

    interest = {
        "products": selected_products,
        "interest_level": random.choice(interest_levels),
        "budget_range": f"{random.randint(50000, 200000)}-{random.randint(200001, 500000)}",
        "urgency_level": random.choice(urgency_levels)
    }

    lead_id = str(uuid.uuid4())
    metadata = {
        "lead_id": lead_id,
        "contact": contact,
        "interest": interest,
        "notes": note,
        "ai_score_of_conversion": random.randint(50, 99)
    }

    lead_text = f"""
    Region: {region}, Language: {language}
    Products: {', '.join(selected_products)}, Interest: {interest['interest_level']}
    Budget: {interest['budget_range']}, Urgency: {interest['urgency_level']}
    Notes: {note}
    """

    return lead_text, metadata

def process_lead(args):
    lead_text, metadata = args
    try:
        vector = get_openai_embedding(lead_text)
        upsert_lead(lead_text, metadata, vector=vector, id=metadata["lead_id"])
        return True
    except Exception as e:
        print(f"❌ Error with lead {metadata['lead_id']}: {e}")
        return False

lead_data = [generate_lead() for _ in range(10000)]
success_count = 0
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_lead, args) for args in lead_data]
    for i, f in enumerate(as_completed(futures), 1):
        if f.result():
            success_count += 1
        if i % 50 == 0:
            print(f"✅ Processed {i} leads...")

print(f"🎯 Finished! Successfully inserted {success_count}/10000 leads.")
