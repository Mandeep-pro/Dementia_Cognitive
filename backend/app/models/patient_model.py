from datetime import datetime
from bson import ObjectId

from app.config.database import db


patients_collection = db["patients"]


def create_patient(
    user_id,
    preferred_name,
    age,
    preferred_language,
    caregiver_id
):
    patient = {
        "user_id": ObjectId(user_id),
        "preferred_name": preferred_name,
        "age": age,
        "preferred_language": preferred_language,
        "caregiver_id": ObjectId(caregiver_id),
        "created_at": datetime.utcnow()
    }

    result = patients_collection.insert_one(patient)

    return str(result.inserted_id)


def find_patient_by_id(patient_id):
    try:
        return patients_collection.find_one({
            "_id": ObjectId(patient_id)
        })
    except Exception:
        return None


def find_patients_by_caregiver(caregiver_id):
    try:
        return list(
            patients_collection.find({
                "caregiver_id": ObjectId(caregiver_id)
            })
        )
    except Exception:
        return []