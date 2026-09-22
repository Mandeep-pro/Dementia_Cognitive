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

    # ------------------------------------------
    # Check caregiver role
    # ------------------------------------------

    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can access the dashboard"
        }, 403

    # ------------------------------------------
    # Find patient
    # ------------------------------------------

    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # ------------------------------------------
    # Check caregiver ownership
    # ------------------------------------------

    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized for this patient"
        }, 403

    # ==========================================
    # PATIENT INFORMATION
    # ==========================================

    patient_data = {
        "id": str(patient["_id"]),
        "user_id": str(patient["user_id"]),
        "preferred_name": patient["preferred_name"],
        "age": patient["age"],
        "preferred_language": patient["preferred_language"]
    }

    # ==========================================
    # GAME RESULTS
    # ==========================================

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

    # ==========================================
    # GAME STATISTICS + ADAPTIVE DIFFICULTY
    # ==========================================

    if results:

        latest_result = results[0]

        current_difficulty = latest_result["difficulty"]
        accuracy = latest_result["accuracy"]

        next_difficulty = get_next_difficulty(
            current_difficulty,
            accuracy
        )

        total_games = len(results)

        average_accuracy = sum(
            result["accuracy"]
            for result in results
        ) / total_games

        highest_score = max(
            result["score"]
            for result in results
        )

    else:

        current_difficulty = "easy"
        accuracy = None
        next_difficulty = "easy"

        total_games = 0
        average_accuracy = None
        highest_score = None

    # ==========================================
    # REMINDERS
    # ==========================================

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

    # ==========================================
    # MEMORY
    # ==========================================

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

    # ==========================================
    # DASHBOARD RESPONSE
    # ==========================================

    return {

        "status": "success",

        "dashboard": {

            # ----------------------------------
            # Patient
            # ----------------------------------

            "patient": patient_data,

            # ----------------------------------
            # Games
            # ----------------------------------

            "games": {

                "total_games": total_games,

                "average_accuracy": (
                    round(average_accuracy, 2)
                    if average_accuracy is not None
                    else None
                ),

                "highest_score": highest_score,

                "latest_accuracy": accuracy,

                "current_difficulty": current_difficulty,

                "next_difficulty": next_difficulty,

                "results": game_results
            },

            # ----------------------------------
            # Reminders
            # ----------------------------------

            "reminders": {

                "count": len(reminder_list),

                "items": reminder_list
            },

            # ----------------------------------
            # Memories
            # ----------------------------------

            "memories": {

                "count": len(memory_list),

                "items": memory_list
            }
        }

    }, 200