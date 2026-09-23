from datetime import datetime
from bson import ObjectId

from app.config.database import db


reminders_collection = db["reminders"]


def create_reminder(
    patient_id,
    title,
    category,
    scheduled_time
):
    pid = ObjectId(str(patient_id)) if ObjectId.is_valid(str(patient_id)) else str(patient_id)
    reminder = {
        "patient_id": pid,
        "title": title,
        "category": category,
        "scheduled_time": scheduled_time,
        "completed": False,
        "created_at": datetime.utcnow()
    }

    result = reminders_collection.insert_one(reminder)

    return str(result.inserted_id)


def find_reminders_by_patient(patient_id):
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

        reminders = reminders_collection.find({
            "patient_id": {"$in": unique_ids}
        }).sort("scheduled_time", 1)

        return list(reminders)

    except Exception as e:
        print("find_reminders_by_patient error:", e)
        return []


def find_reminder_by_id(reminder_id):
    try:
        if not reminder_id:
            return None
        sid = str(reminder_id)
        if ObjectId.is_valid(sid):
            found = reminders_collection.find_one({"_id": ObjectId(sid)})
            if found:
                return found
        return reminders_collection.find_one({"_id": sid})
    except Exception:
        return None


def update_reminder_status(reminder_id, completed):
    try:
        result = reminders_collection.update_one(
            {"_id": ObjectId(reminder_id)},
            {
                "$set": {
                    "completed": completed
                }
            }
        )

        return result.modified_count > 0

    except Exception:
        return False


def delete_reminder(reminder_id):
    try:
        result = reminders_collection.delete_one({
            "_id": ObjectId(reminder_id)
        })

        return result.deleted_count > 0

    except Exception:
        return False