from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId  
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["test"]  # or "GromoPlus"
globalleads_collection = db["globalleads"]
gps_collection = db["gps"]
def get_lead_by_id(mongo_id: str):
    try:
        # UUIDs are stored as string _id, no need for ObjectId
        lead = globalleads_collection.find_one({"_id": mongo_id})
        if not lead:
            raise ValueError(f"No lead found with Mongo _id: {mongo_id}")
        return lead
    except Exception as e:
        raise ValueError(f"Error fetching lead: {e}")
def get_gp_profile_by_id(gp_id: str):
    try:
        profile = gps_collection.find_one({"_id": ObjectId(gp_id)})
        if not profile:
            raise ValueError(f"GP with id {gp_id} not found.")
        return profile
    except Exception as e:
        raise ValueError(f"Error fetching GP: {e}")