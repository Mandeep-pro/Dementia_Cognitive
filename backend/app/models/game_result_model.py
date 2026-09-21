from datetime import datetime
from bson import ObjectId

from app.config.database import db


game_results_collection = db["game_results"]


def create_game_result(
    patient_id,
    game_id,
    score,
    accuracy,
    time_taken,
    difficulty
):
    game_result = {
        "patient_id": ObjectId(patient_id),
        "game_id": game_id,
        "score": score,
        "accuracy": accuracy,
        "time_taken": time_taken,
        "difficulty": difficulty,
        "created_at": datetime.utcnow()
    }

    result = game_results_collection.insert_one(game_result)

    return str(result.inserted_id)


def find_results_by_patient(patient_id):
    try:
        results = game_results_collection.find({
            "patient_id": ObjectId(patient_id)
        }).sort("created_at", -1)

        return list(results)

    except Exception:
        return []