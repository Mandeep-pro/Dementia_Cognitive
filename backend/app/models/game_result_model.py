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
    pid = ObjectId(str(patient_id)) if ObjectId.is_valid(str(patient_id)) else str(patient_id)
    game_result = {
        "patient_id": pid,
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
        if not patient_id:
            return []

        from app.models.patient_model import find_patient_by_id, find_patient_by_user_id

        sid = str(patient_id)
        ids_to_match = [sid]
        if ObjectId.is_valid(sid):
            ids_to_match.append(ObjectId(sid))

        # Also find patient document to include both patient._id and patient.user_id
        pat = find_patient_by_id(sid)
        if not pat:
            pat = find_patient_by_user_id(sid)

        if pat:
            p_id = pat["_id"]
            ids_to_match.extend([p_id, str(p_id)])
            if pat.get("user_id"):
                u_id = pat["user_id"]
                ids_to_match.extend([u_id, str(u_id)])

        # Deduplicate
        unique_ids = []
        for item in ids_to_match:
            if item not in unique_ids:
                unique_ids.append(item)

        results = game_results_collection.find({
            "patient_id": {"$in": unique_ids}
        }).sort("created_at", -1)

        return list(results)

    except Exception as e:
        print("find_results_by_patient error:", e)
        return []