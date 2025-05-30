import random
import uuid
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from qdrant_utils import  upsert_lead, client
from embedding_utils import get_openai_embedding
from qdrant_client.http.exceptions import UnexpectedResponse

# Load notes
lead_notes_path = Path("templates_db/lead.txt")
lead_notes = [line.strip() for line in lead_notes_path.read_text().splitlines() if line.strip()]

# Constants
states = [
    "Maharashtra", "Uttar Pradesh", "Punjab", "Tamil Nadu", "Gujarat",
    "Rajasthan", "Karnataka", "Kerala", "Bihar", "West Bengal",
    "Telangana", "Andhra Pradesh", "Madhya Pradesh", "Odisha", "Chhattisgarh",
    "Jharkhand", "Haryana", "Assam", "Uttarakhand", "Himachal Pradesh"
]
products = [
    "credit_card", "personal_loan", "demat_account", "investment", "saving_account",
    "instant_deals", "credit_line", "business_loan", "subscription", "credit"
]

interest_levels = ["low", "medium", "high"]
occupations = [
    "Engineer", "Teacher", "Salesperson", "Clerk", "Manager", "Entrepreneur",
    "Accountant", "Doctor", "Freelancer", "Student", "Software Developer", "Consultant"
]

income_brackets = [
    "1-2 LPA", "2-4 LPA", "4-6 LPA", "6-8 LPA", "8-10 LPA", "10-15 LPA", "15+ LPA"
]

first_names = [
    "Ravi", "Neha", "Amit", "Pooja", "Karan", "Priya", "Sneha", "Ankur", "Megha", "Nikhil",
    "Divya", "Rohit", "Sonal", "Vikas", "Shruti", "Tanya", "Arjun", "Isha", "Manish", "Reena"
]

last_names = [
    "Kumar", "Verma", "Sharma", "Patel", "Singh", "Yadav", "Joshi", "Das", "Reddy", "Bose",
    "Ghosh", "Naidu", "Pillai", "Chatterjee", "Agarwal", "Malhotra", "Mishra", "Pandey", "Thakur", "Dube"
]

# Ensure collection exists
# try:
#     client.get_collection("gromo_leads")
#     print("📦 Collection already exists.")
# except UnexpectedResponse:
#     create_collection()
#     print("🆕 Created collection: gromo_leads")

def generate_lead():
    lead_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    note = random.choice(lead_notes)
    selected_products = random.sample(products, k=random.randint(1, 2))
    state = random.choice(states)

    lead = {
        "_id": lead_id,
        "referrer_gp_id": f"GP{random.randint(100,999)}",
        "buyer_gp_ids": [f"GP{random.randint(100,999)}", f"GP{random.randint(100,999)}"],
        "contact": {
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "phone": f"+91{random.randint(7000000000, 9999999999)}"
        },
        "interest": {
            "products": selected_products,
            "interest_level": random.choice(interest_levels)
        },
        "notes": note,
        "personal_data": {
            "occupation": random.choice(occupations),
            "age": random.randint(22, 50),
            "income": random.choice(income_brackets),
            "state": state
        },
        "summary": f"{state}-based {occupations[0].lower()} interested in {selected_products[0]}.",
        "is_sellable": True,
        "status": "NEW",
        "createdAt": now,
        "updatedAt": now
    }

    lead_text = f"""
    Name: {lead['contact']['name']}, Phone: {lead['contact']['phone']}
    Age: {lead['personal_data']['age']}, State: {lead['personal_data']['state']}, 
    Occupation: {lead['personal_data']['occupation']}, Income: {lead['personal_data']['income']}
    Interested in: {', '.join(lead['interest']['products'])}, Interest Level: {lead['interest']['interest_level']}
    Notes: {lead['notes']}
    Summary: {lead['summary']}
    """

    return lead_text.strip(), lead

def process_lead(args):
    lead_text, metadata = args
    try:
        vector = get_openai_embedding(lead_text)
        upsert_lead(text=lead_text, metadata=metadata, id=metadata["_id"], vector=vector)
        return True
    except Exception as e:
        print(f"❌ Failed for {metadata['_id']}: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Generating and uploading 1 sample lead...")
    test_data = [generate_lead() for _ in range(500)]  

    success = 0
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_lead, args) for args in test_data]
        for f in as_completed(futures):
            if f.result():
                success += 1

    print(f"✅ Finished uploading {success}/{len(test_data)} leads.")
