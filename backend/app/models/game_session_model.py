from datetime import datetime, timezone
from bson import ObjectId

from app.config.database import db


game_sessions_collection = db["game_sessions"]


def create_game_session(
    patient_id,
    game_id,
    difficulty,
    questions
):
    session = {
        "patient_id": ObjectId(patient_id),
        "game_id": game_id,
        "difficulty": difficulty,
        "questions": questions,
        "created_at": datetime.now(timezone.utc),
        "completed": False
    }

    result = game_sessions_collection.insert_one(session)

    return str(result.inserted_id)


def find_game_session(session_id):
    try:
        return game_sessions_collection.find_one(
            {"_id": ObjectId(session_id)}
        )
    except Exception:
        return None


def complete_game_session(session_id):
    try:
        result = game_sessions_collection.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "completed": True,
                    "completed_at": datetime.now(timezone.utc)
                }
            }
        )

        return result.modified_count > 0

    except Exception:
        return False