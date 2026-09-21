from datetime import datetime
from bson import ObjectId
from app.config.database import db


users_collection = db["users"]


def create_user(name, email, password_hash, role):
    user = {
        "name": name,
        "email": email.lower().strip(),
        "password_hash": password_hash,
        "role": role,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user)

    return str(result.inserted_id)


def find_user_by_email(email):
    return users_collection.find_one({
        "email": email.lower().strip()
    })


def find_user_by_id(user_id):
    try:
        return users_collection.find_one({
            "_id": ObjectId(user_id)
        })
    except Exception:
        return None