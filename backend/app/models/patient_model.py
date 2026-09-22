from datetime import datetime
from bson import ObjectId

from app.config.database import db


patients_collection = db["patients"]


# ==========================================
# CREATE PATIENT
# ==========================================

def create_patient(
    user_id,
    preferred_name,
    age,
    preferred_language,
    caregiver_id,
    family=None,
    favorite_things=None,
    daily_routine=None,
    important_places=None,
    personal_memories=None
):
    patient = {
        "user_id": ObjectId(user_id),
        "preferred_name": preferred_name,
        "age": age,
        "preferred_language": preferred_language,
        "caregiver_id": ObjectId(caregiver_id),

        # Optional personal information
        "family": family or [],
        "favorite_things": favorite_things or [],
        "daily_routine": daily_routine or [],
        "important_places": important_places or [],
        "personal_memories": personal_memories or [],

        "created_at": datetime.utcnow()
    }

    result = patients_collection.insert_one(patient)

    return str(result.inserted_id)


# ==========================================
# FIND PATIENT BY ID
# ==========================================

def find_patient_by_id(patient_id):
    try:
        return patients_collection.find_one({
            "_id": ObjectId(patient_id)
        })
    except Exception:
        return None


# ==========================================
# FIND PATIENTS BY CAREGIVER
# ==========================================

def find_patients_by_caregiver(caregiver_id):
    try:
        return list(
            patients_collection.find({
                "caregiver_id": ObjectId(caregiver_id)
            })
        )
    except Exception:
        return []


def update_patient(patient_id, updates):
    try:
        result = patients_collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": updates}
        )

        return result.modified_count > 0

    except Exception:
        return False    