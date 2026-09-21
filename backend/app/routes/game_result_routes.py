from flask import Blueprint, request, g

from app.middleware.auth_middleware import token_required
from app.models.patient_model import find_patient_by_id
from app.services.game_service import save_game_result
from app.services.adaptive_service import get_next_difficulty

game_result_bp = Blueprint("game_result", __name__)


# ==========================================
# CREATE GAME RESULT
# ==========================================

@game_result_bp.route("/", methods=["POST"])
@token_required
def create_result():

    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    required_fields = [
        "patient_id",
        "game_id",
        "score",
        "accuracy",
        "time_taken",
        "difficulty"
    ]

    if not all(field in data for field in required_fields):
        return {
            "status": "error",
            "message": "All game result fields are required"
        }, 400

    patient_id = data["patient_id"]

    # Find patient
    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Only the patient's caregiver can submit results
    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized for this patient"
        }, 403

    try:
        score = int(data["score"])
        accuracy = float(data["accuracy"])
        time_taken = float(data["time_taken"])
    except (ValueError, TypeError):
        return {
            "status": "error",
            "message": "Score, accuracy and time_taken must be numbers"
        }, 400

    result, error = save_game_result(
        patient_id=patient_id,
        game_id=data["game_id"],
        score=score,
        accuracy=accuracy,
        time_taken=time_taken,
        difficulty=data["difficulty"]
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 400

    return {
        "status": "success",
        "message": "Game result saved successfully",
        "result": result
    }, 201

# ==========================================
# GET PATIENT GAME HISTORY
# ==========================================

@game_result_bp.route("/<patient_id>", methods=["GET"])
@token_required
def get_patient_results(patient_id):

    # Make sure the patient exists
    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Only the patient's caregiver can view results
    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized for this patient"
        }, 403

    from app.models.game_result_model import find_results_by_patient

    results = find_results_by_patient(patient_id)

    result_list = []

    for result in results:
        result_list.append({
            "id": str(result["_id"]),
            "patient_id": str(result["patient_id"]),
            "game_id": result["game_id"],
            "score": result["score"],
            "accuracy": result["accuracy"],
            "time_taken": result["time_taken"],
            "difficulty": result["difficulty"],
            "created_at": result["created_at"].isoformat()
        })

    return {
        "status": "success",
        "count": len(result_list),
        "results": result_list
    }, 200
# ==========================================
# GET NEXT GAME DIFFICULTY
# ==========================================

@game_result_bp.route(
    "/<patient_id>/next-difficulty",
    methods=["GET"]
)
@token_required
def get_next_game_difficulty(patient_id):

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

    from app.models.game_result_model import find_results_by_patient

    results = find_results_by_patient(patient_id)

    # No previous game result
    if not results:
        return {
            "status": "success",
            "current_difficulty": "easy",
            "next_difficulty": "easy",
            "reason": "No previous game result"
        }, 200

    latest_result = results[0]

    current_difficulty = latest_result["difficulty"]
    accuracy = latest_result["accuracy"]

    next_difficulty = get_next_difficulty(
        current_difficulty=current_difficulty,
        accuracy=accuracy
    )

    return {
        "status": "success",
        "current_difficulty": current_difficulty,
        "accuracy": accuracy,
        "next_difficulty": next_difficulty
    }, 200