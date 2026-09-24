from flask import Blueprint, request, g

from app.middleware.auth_middleware import token_required
from app.models.patient_model import find_patient_by_id
from app.services.game_service import save_game_result
from app.services.adaptive_service import recommend_next_difficulty

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

    patient_id = data.get("patient_id")

    # Find patient by caller's token, patient _id, or user_id
    from app.models.patient_model import find_patient_by_user_id
    patient = None

    if g.user.get("role") == "patient":
        # Always prioritize the authenticated patient's own profile
        patient = find_patient_by_user_id(g.user["user_id"])
        if not patient and patient_id:
            patient = find_patient_by_id(patient_id)
            if not patient:
                patient = find_patient_by_user_id(patient_id)
    else:
        # Caregiver submitting or testing
        if patient_id:
            patient = find_patient_by_id(patient_id)
            if not patient:
                patient = find_patient_by_user_id(patient_id)

    if not patient and g.user.get("role") == "patient":
        try:
            from app.models.user_model import find_user_by_id
            from app.models.patient_model import patients_collection
            from bson import ObjectId
            from datetime import datetime, timezone

            u = find_user_by_id(g.user["user_id"])
            u_name = u["name"] if u else "Friend"
            res = patients_collection.insert_one({
                "user_id": ObjectId(g.user["user_id"]),
                "preferred_name": u_name,
                "age": None,
                "preferred_language": "English",
                "caregiver_id": None,
                "family": [],
                "favorite_things": [],
                "daily_routine": [],
                "important_places": [],
                "personal_memories": [],
                "created_at": datetime.now(timezone.utc)
            })
            patient = patients_collection.find_one({"_id": res.inserted_id})
        except Exception as e:
            print("Auto-create patient failed in game_result_routes:", e)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Allow caregiver or the patient themself to submit results
    caller_id = str(g.user["user_id"])
    is_caregiver = str(patient.get("caregiver_id", "")) == caller_id
    is_patient = str(patient.get("user_id", "")) == caller_id
    is_patient_self = str(patient.get("_id", "")) == caller_id

    if not (is_caregiver or is_patient or is_patient_self):
        # If caller is caregiver and patient has no caregiver assigned, auto-link
        if g.user.get("role") == "caregiver" and not patient.get("caregiver_id"):
            from app.models.patient_model import update_patient
            from bson import ObjectId
            update_patient(str(patient["_id"]), {"caregiver_id": ObjectId(caller_id)})
            is_caregiver = True
        else:
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

    actual_patient_id = str(patient["_id"])

    result, error = save_game_result(
        patient_id=actual_patient_id,
        game_id=data["game_id"],
        score=score,
        accuracy=accuracy,
        time_taken=time_taken,
        difficulty=data.get("difficulty", "easy")
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
    from app.models.patient_model import find_patient_by_user_id
    patient = find_patient_by_id(patient_id)
    if not patient:
        patient = find_patient_by_user_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Allow caregiver or the patient themself to view results
    is_caregiver = str(patient.get("caregiver_id", "")) == g.user["user_id"]
    is_patient = str(patient.get("user_id", "")) == g.user["user_id"]

    if not (is_caregiver or is_patient):
        return {
            "status": "error",
            "message": "You are not authorized for this patient"
        }, 403

    from app.models.game_result_model import find_results_by_patient

    actual_patient_id = str(patient["_id"])
    results = find_results_by_patient(actual_patient_id)

    result_list = []

    for result in results:
        created_at_val = result.get("created_at")
        created_at_str = created_at_val.isoformat() if hasattr(created_at_val, "isoformat") else str(created_at_val or "")

        result_list.append({
            "id": str(result["_id"]),
            "patient_id": str(result.get("patient_id", "")),
            "game_id": result.get("game_id", "brain-boost"),
            "score": result.get("score", 0),
            "accuracy": result.get("accuracy", 0),
            "time_taken": result.get("time_taken", 0),
            "difficulty": result.get("difficulty", "easy"),
            "created_at": created_at_str
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

    from app.models.patient_model import find_patient_by_user_id
    patient = find_patient_by_id(patient_id)
    if not patient:
        patient = find_patient_by_user_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    is_caregiver = str(patient.get("caregiver_id", "")) == g.user["user_id"]
    is_patient = str(patient.get("user_id", "")) == g.user["user_id"]

    if not (is_caregiver or is_patient):
        return {
            "status": "error",
            "message": "You are not authorized for this patient"
        }, 403

    from app.models.game_result_model import find_results_by_patient

    actual_patient_id = str(patient["_id"])
    results = find_results_by_patient(actual_patient_id)

    # No previous game result
    if not results:
        return {
            "status": "success",
            "current_difficulty": "easy",
            "next_difficulty": "easy",
            "reason": "No previous game result"
        }, 200

    latest_result = results[0]

    current_difficulty = latest_result.get("difficulty", "easy")
    accuracy = latest_result.get("accuracy", 0)

    next_difficulty, recommendation_source, confidence = recommend_next_difficulty(
        patient=patient,
        current_difficulty=current_difficulty,
        accuracy=accuracy,
        time_taken=latest_result.get("time_taken", 0)
    )

    return {
        "status": "success",
        "current_difficulty": current_difficulty,
        "accuracy": accuracy,
        "next_difficulty": next_difficulty,
        "recommendation_source": recommendation_source,
        "confidence": confidence
    }, 200