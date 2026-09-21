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
    reminder = {
        "patient_id": ObjectId(patient_id),
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
        reminders = reminders_collection.find({
            "patient_id": ObjectId(patient_id)
        }).sort("scheduled_time", 1)

        return list(reminders)

    except Exception:
        return []


def find_reminder_by_id(reminder_id):
    try:
        return reminders_collection.find_one({
            "_id": ObjectId(reminder_id)
        })
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