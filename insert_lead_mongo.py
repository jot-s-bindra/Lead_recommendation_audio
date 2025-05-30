from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["test"]  # or "GromoPlus" if that's the correct one
collection = db["globalleads"]

def insert_sample_lead():
    lead_id = str(uuid.uuid4())  # Generate a valid UUID

    lead = {
        "_id": lead_id,  # Use UUID as the Mongo _id
        "referrer_gp_id": None,
        "buyer_gp_ids": [],
        "contact": {
            "name": "Akshay",
            "phone": "+919876543210"
        },
        "interest": {
            "products": ["credit_card", "home_loan"],
            "interest_level": "high"
        },
        "personal_data": {
            "occupation": "Engineer",
            "age": 30,
            "income": 75000,
            "state": "Delhi"
        },
        "summary": "Interested in high value products with online proficiency.",
        "notes": "Wants best interest rates. Experienced with credit products.",
        "status": "NEW",
        "isSellable": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    collection.insert_one(lead)
    print(f"✅ Lead inserted to MongoDB with UUID _id: {lead_id}")
    return lead_id

if __name__ == "__main__":
    insert_sample_lead()
