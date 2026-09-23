from flask import Blueprint, request, g

from app.middleware.auth_middleware import token_required

from app.models.patient_model import (
    find_patient_by_id,
    find_patients_by_caregiver,
    find_patient_by_user_id,
    update_patient
)

from app.services.patient_service import create_patient_for_caregiver


patient_bp = Blueprint("patient", __name__)


# ==========================================
# CREATE PATIENT
# ==========================================

@patient_bp.route("/", methods=["POST"])
@token_required
def create_patient():

    # Only caregivers can create patient profiles
    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can create patients"
        }, 403

    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    required_fields = [
        "name",
        "email",
        "password",
        "preferred_name",
        "age",
        "preferred_language"
    ]

    if not all(field in data for field in required_fields):
        return {
            "status": "error",
            "message": "All patient fields are required"
        }, 400

    try:
        age = int(data["age"])
    except (ValueError, TypeError):
        return {
            "status": "error",
            "message": "Age must be a valid number"
        }, 400

    if age < 1 or age > 120:
        return {
            "status": "error",
            "message": "Age must be between 1 and 120"
        }, 400

    # Optional personal information
    family = data.get("family", [])
    favorite_things = data.get("favorite_things", [])
    daily_routine = data.get("daily_routine", [])
    important_places = data.get("important_places", [])
    personal_memories = data.get("personal_memories", [])

    result, error = create_patient_for_caregiver(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        preferred_name=data["preferred_name"],
        age=age,
        preferred_language=data["preferred_language"],
        caregiver_id=g.user["user_id"],

        # Personalization data
        family=family,
        favorite_things=favorite_things,
        daily_routine=daily_routine,
        important_places=important_places,
        personal_memories=personal_memories
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 400

    return {
        "status": "success",
        "message": "Patient created successfully",
        "patient": {
            "id": str(result.get("patient_id") or result.get("id")),
            "patient_id": str(result.get("patient_id") or result.get("id")),
            "user_id": str(result.get("user_id", ""))
        }
    }, 201


# ==========================================
# GET CURRENT PATIENT PROFILE (ME)
# ==========================================

@patient_bp.route("/me", methods=["GET"])
@token_required
def get_my_patient_profile():

    patient = find_patient_by_user_id(g.user["user_id"])

    if not patient and g.user.get("role") == "patient":
        try:
            from app.models.user_model import find_user_by_id
            from app.models.patient_model import patients_collection
            from bson import ObjectId
            from datetime import datetime, timezone

            user = find_user_by_id(g.user["user_id"])
            user_name = user["name"] if user else "Friend"
            res = patients_collection.insert_one({
                "user_id": ObjectId(g.user["user_id"]),
                "preferred_name": user_name,
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
            print("Auto-create patient failed:", e)

    if not patient and g.user.get("role") == "caregiver":
        caregiver_patients = find_patients_by_caregiver(g.user["user_id"])
        if caregiver_patients:
            patient = caregiver_patients[0]
        else:
            from app.models.user_model import find_user_by_id
            user = find_user_by_id(g.user["user_id"])
            user_name = user["name"] if user else "Caregiver"
            return {
                "status": "success",
                "patient": {
                    "id": str(user["_id"]) if user else g.user["user_id"],
                    "user_id": g.user["user_id"],
                    "name": user_name,
                    "preferred_name": user_name,
                    "email": user["email"] if user else "",
                    "role": "caregiver",
                    "caregiver_name": user_name,
                    "family": [],
                    "favorite_things": [],
                    "daily_routine": [],
                    "important_places": [],
                    "personal_memories": []
                }
            }, 200

    if not patient:
        return {
            "status": "error",
            "message": "No patient profile associated with this account"
        }, 404

    created_at_val = patient.get("created_at")
    created_at_str = created_at_val.isoformat() if hasattr(created_at_val, "isoformat") else str(created_at_val or "")

    return {
        "status": "success",
        "patient": {
            "id": str(patient["_id"]),
            "user_id": str(patient["user_id"]),
            "preferred_name": patient.get("preferred_name", ""),
            "age": patient.get("age"),
            "preferred_language": patient.get("preferred_language", "English"),
            "caregiver_id": str(patient["caregiver_id"]) if patient.get("caregiver_id") else None,

            # Personalization data
            "family": patient.get("family", []),
            "favorite_things": patient.get("favorite_things", []),
            "daily_routine": patient.get("daily_routine", []),
            "important_places": patient.get("important_places", []),
            "personal_memories": patient.get("personal_memories", []),

            "created_at": created_at_str
        }
    }, 200


# ==========================================
# GET PATIENT
# ==========================================

@patient_bp.route("/<patient_id>", methods=["GET"])
@token_required
def get_patient(patient_id):

    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Allow access if caller is the caregiver OR the patient themself
    is_caregiver = str(patient.get("caregiver_id", "")) == g.user["user_id"]
    is_patient = str(patient.get("user_id", "")) == g.user["user_id"]

    if not (is_caregiver or is_patient):
        return {
            "status": "error",
            "message": "You are not authorized to access this patient"
        }, 403

    created_at_val = patient.get("created_at")
    created_at_str = created_at_val.isoformat() if hasattr(created_at_val, "isoformat") else str(created_at_val or "")

    return {
        "status": "success",
        "patient": {
            "id": str(patient["_id"]),
            "user_id": str(patient.get("user_id", "")),
            "preferred_name": patient.get("preferred_name", ""),
            "age": patient.get("age"),
            "preferred_language": patient.get("preferred_language", "English"),
            "caregiver_id": str(patient["caregiver_id"]) if patient.get("caregiver_id") else None,

            # Personalization data
            "family": patient.get("family", []),
            "favorite_things": patient.get("favorite_things", []),
            "daily_routine": patient.get("daily_routine", []),
            "important_places": patient.get("important_places", []),
            "personal_memories": patient.get("personal_memories", []),

            "created_at": created_at_str
        }
    }, 200


# ==========================================
# GET ALL PATIENTS FOR CAREGIVER
# ==========================================

@patient_bp.route("/", methods=["GET"])
@token_required
def get_patients():

    # Only caregivers can access their patient list
    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can access patients"
        }, 403

    try:
        patients = find_patients_by_caregiver(
            g.user["user_id"]
        )

        patient_list = []

        for patient in patients:
            created_at_val = patient.get("created_at")
            created_at_str = created_at_val.isoformat() if hasattr(created_at_val, "isoformat") else str(created_at_val or "")

            patient_list.append({
                "id": str(patient["_id"]),
                "user_id": str(patient.get("user_id", "")),
                "preferred_name": patient.get("preferred_name", ""),
                "age": patient.get("age"),
                "preferred_language": patient.get("preferred_language", "English"),
                "caregiver_id": str(patient["caregiver_id"]) if patient.get("caregiver_id") else None,

                # Personalization data
                "family": patient.get("family", []),
                "favorite_things": patient.get("favorite_things", []),
                "daily_routine": patient.get("daily_routine", []),
                "important_places": patient.get("important_places", []),
                "personal_memories": patient.get("personal_memories", []),

                "created_at": created_at_str
            })

        return {
            "status": "success",
            "count": len(patient_list),
            "patients": patient_list
        }, 200

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve patients: {str(e)}"
        }, 500




# ==========================================
# UPDATE PATIENT PERSONAL INFORMATION
# ==========================================

@patient_bp.route("/<patient_id>", methods=["PUT"])
@token_required
def update_patient_profile(patient_id):

    # Only caregivers can update patient profiles
    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can update patients"
        }, 403

    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Make sure this patient belongs to the logged-in caregiver
    if str(patient.get("caregiver_id", "")) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized to update this patient"
        }, 403

    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    allowed_fields = [
        "preferred_name",
        "age",
        "preferred_language",
        "family",
        "favorite_things",
        "daily_routine",
        "important_places",
        "personal_memories"
    ]

    updates = {}

    for field in allowed_fields:
        if field in data:
            updates[field] = data[field]

    if not updates:
        return {
            "status": "error",
            "message": "No valid fields provided for update"
        }, 400

    # Validate age if it is being updated
    if "age" in updates:
        try:
            age = int(updates["age"])
        except (ValueError, TypeError):
            return {
                "status": "error",
                "message": "Age must be a valid number"
            }, 400

        if age < 1 or age > 120:
            return {
                "status": "error",
                "message": "Age must be between 1 and 120"
            }, 400

        updates["age"] = age

    update_patient(patient_id, updates)

    return {
        "status": "success",
        "message": "Patient updated successfully"
    }, 200