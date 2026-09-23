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
    pid = ObjectId(str(patient_id)) if ObjectId.is_valid(str(patient_id)) else str(patient_id)
    memory = {
        "patient_id": pid,
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
        if not patient_id:
            return []

        from app.models.patient_model import find_patient_by_id, find_patient_by_user_id

        sid = str(patient_id)
        ids_to_match = [sid]
        if ObjectId.is_valid(sid):
            ids_to_match.append(ObjectId(sid))

        pat = find_patient_by_id(sid)
        if not pat:
            pat = find_patient_by_user_id(sid)

        if pat:
            p_id = pat["_id"]
            ids_to_match.extend([p_id, str(p_id)])
            if pat.get("user_id"):
                u_id = pat["user_id"]
                ids_to_match.extend([u_id, str(u_id)])

        unique_ids = []
        for item in ids_to_match:
            if item not in unique_ids:
                unique_ids.append(item)

        memories = memories_collection.find({
            "patient_id": {"$in": unique_ids}
        }).sort("created_at", -1)

        return list(memories)

    except Exception as e:
        print("find_memories_by_patient error:", e)
        return []


def find_memory_by_id(memory_id):
    try:
        if not memory_id:
            return None
        sid = str(memory_id)
        if ObjectId.is_valid(sid):
            found = memories_collection.find_one({"_id": ObjectId(sid)})
            if found:
                return found
        return memories_collection.find_one({"_id": sid})
    except Exception:
        return None


def delete_memory(memory_id):
    try:
        if not memory_id:
            return False
        sid = str(memory_id)
        target = ObjectId(sid) if ObjectId.is_valid(sid) else sid
        result = memories_collection.delete_one({
            "_id": target
        })

        return result.deleted_count > 0

    except Exception:
        return False