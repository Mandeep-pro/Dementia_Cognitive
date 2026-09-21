from flask import Blueprint, g

from app.middleware.auth_middleware import token_required
from app.models.patient_model import find_patient_by_id
from app.models.game_result_model import find_results_by_patient
from app.models.reminder_model import find_reminders_by_patient
from app.models.memory_model import find_memories_by_patient
from app.services.adaptive_service import get_next_difficulty


caregiver_bp = Blueprint("caregiver", __name__)


# ==========================================
# CAREGIVER DASHBOARD
# ==========================================

@caregiver_bp.route("/dashboard/<patient_id>", methods=["GET"])
@token_required
def get_dashboard(patient_id):

    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can access the dashboard"
        }, 403

    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized for this patient"
        }, 403

    # ------------------------------------------
    # Patient information
    # ------------------------------------------

    patient_data = {
        "id": str(patient["_id"]),
        "user_id": str(patient["user_id"]),
        "preferred_name": patient["preferred_name"],
        "age": patient["age"],
        "preferred_language": patient["preferred_language"]
    }

    # ------------------------------------------
    # Game results
    # ------------------------------------------

    results = find_results_by_patient(patient_id)

    game_results = []

    for result in results:
        game_results.append({
            "id": str(result["_id"]),
            "game_id": result["game_id"],
            "score": result["score"],
            "accuracy": result["accuracy"],
            "time_taken": result["time_taken"],
            "difficulty": result["difficulty"],
            "created_at": result["created_at"].isoformat()
        })

    # ------------------------------------------
    # Adaptive difficulty
    # ------------------------------------------

    if results:
        latest_result = results[0]

        current_difficulty = latest_result["difficulty"]
        accuracy = latest_result["accuracy"]

        next_difficulty = get_next_difficulty(
            current_difficulty,
            accuracy
        )
    else:
        current_difficulty = "easy"
        accuracy = None
        next_difficulty = "easy"

    # ------------------------------------------
    # Reminders
    # ------------------------------------------

    reminders = find_reminders_by_patient(patient_id)

    reminder_list = []

    for reminder in reminders:
        reminder_list.append({
            "id": str(reminder["_id"]),
            "title": reminder["title"],
            "category": reminder["category"],
            "scheduled_time": reminder["scheduled_time"],
            "completed": reminder["completed"]
        })

    # ------------------------------------------
    # Memories
    # ------------------------------------------

    memories = find_memories_by_patient(patient_id)

    memory_list = []

    for memory in memories:
        memory_list.append({
            "id": str(memory["_id"]),
            "title": memory["title"],
            "description": memory["description"],
            "category": memory["category"],
            "image_url": memory.get("image_url")
        })

    # ------------------------------------------
    # Dashboard response
    # ------------------------------------------

    return {
        "status": "success",
        "dashboard": {
            "patient": patient_data,

            "games": {
                "total_results": len(game_results),
                "latest_accuracy": accuracy,
                "current_difficulty": current_difficulty,
                "next_difficulty": next_difficulty,
                "results": game_results
            },

            "reminders": {
                "count": len(reminder_list),
                "items": reminder_list
            },

            "memories": {
                "count": len(memory_list),
                "items": memory_list
            }
        }
    }, 200