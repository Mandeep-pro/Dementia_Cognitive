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
        if not patient_id:
            return None
        sid = str(patient_id)
        if ObjectId.is_valid(sid):
            found = patients_collection.find_one({"_id": ObjectId(sid)})
            if found:
                return found
        return patients_collection.find_one({"_id": sid})
    except Exception:
        return None


# ==========================================
# FIND PATIENTS BY CAREGIVER
# ==========================================

def find_patients_by_caregiver(caregiver_id):
    try:
        if not caregiver_id:
            return []
        sid = str(caregiver_id)
        ids_to_match = [sid]
        if ObjectId.is_valid(sid):
            ids_to_match.append(ObjectId(sid))

        return list(
            patients_collection.find({
                "caregiver_id": {"$in": ids_to_match}
            })
        )
    except Exception:
        return []


def update_patient(patient_id, updates):
    try:
        if not patient_id:
            return False
        sid = str(patient_id)
        target = ObjectId(sid) if ObjectId.is_valid(sid) else sid
        result = patients_collection.update_one(
            {"_id": target},
            {"$set": updates}
        )

        return result.modified_count > 0

    except Exception:
        return False


# ==========================================
# FIND PATIENT BY USER ID
# ==========================================

def find_patient_by_user_id(user_id):
    try:
        if not user_id:
            return None
        sid = str(user_id)
        ids_to_match = [sid]
        if ObjectId.is_valid(sid):
            ids_to_match.append(ObjectId(sid))

        return patients_collection.find_one({
            "user_id": {"$in": ids_to_match}
        })
    except Exception:
        return None