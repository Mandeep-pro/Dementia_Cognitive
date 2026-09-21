from datetime import datetime
from bson import ObjectId

from app.config.database import db


memories_collection = db["memories"]


def create_memory(
    patient_id,
    title,
    description,
    category,
    image_url=None
):
    memory = {
        "patient_id": ObjectId(patient_id),
        "title": title,
        "description": description,
        "category": category,
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }

    result = memories_collection.insert_one(memory)

    return str(result.inserted_id)


def find_memories_by_patient(patient_id):
    try:
        memories = memories_collection.find({
            "patient_id": ObjectId(patient_id)
        }).sort("created_at", -1)

        return list(memories)

    except Exception:
        return []


def find_memory_by_id(memory_id):
    try:
        return memories_collection.find_one({
            "_id": ObjectId(memory_id)
        })
    except Exception:
        return None


def delete_memory(memory_id):
    try:
        result = memories_collection.delete_one({
            "_id": ObjectId(memory_id)
        })

        return result.deleted_count > 0

    except Exception:
        return False