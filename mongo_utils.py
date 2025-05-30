from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["test"]  # or "GromoPlus"
globalleads_collection = db["globalleads"]

def get_lead_by_id(mongo_id: str):
    try:
        # UUIDs are stored as string _id, no need for ObjectId
        lead = globalleads_collection.find_one({"_id": mongo_id})
        if not lead:
            raise ValueError(f"No lead found with Mongo _id: {mongo_id}")
        return lead
    except Exception as e:
        raise ValueError(f"Error fetching lead: {e}")
