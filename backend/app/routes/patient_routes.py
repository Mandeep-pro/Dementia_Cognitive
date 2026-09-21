from flask import Blueprint, request, g

from app.models.patient_model import find_patient_by_id
from app.middleware.auth_middleware import token_required
from app.services.patient_service import create_patient_for_caregiver

from app.models.patient_model import (
    find_patient_by_id,
    find_patients_by_caregiver
)

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

    result, error = create_patient_for_caregiver(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        preferred_name=data["preferred_name"],
        age=age,
        preferred_language=data["preferred_language"],
        caregiver_id=g.user["user_id"]
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 400

    return {
        "status": "success",
        "message": "Patient created successfully",
        "patient": result
    }, 201


# ==========================================
# GET PATIENT
# ==========================================

@patient_bp.route("/<patient_id>", methods=["GET"])
@token_required
def get_patient(patient_id):

    # Only caregivers can access patient profiles
    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can access patient profiles"
        }, 403

    patient = find_patient_by_id(patient_id)

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    # Make sure this patient belongs to the logged-in caregiver
    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized to access this patient"
        }, 403

    return {
        "status": "success",
        "patient": {
            "id": str(patient["_id"]),
            "user_id": str(patient["user_id"]),
            "preferred_name": patient["preferred_name"],
            "age": patient["age"],
            "preferred_language": patient["preferred_language"],
            "caregiver_id": str(patient["caregiver_id"]),
            "created_at": patient["created_at"].isoformat()
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

    patients = find_patients_by_caregiver(
        g.user["user_id"]
    )

    patient_list = []

    for patient in patients:
        patient_list.append({
            "id": str(patient["_id"]),
            "user_id": str(patient["user_id"]),
            "preferred_name": patient["preferred_name"],
            "age": patient["age"],
            "preferred_language": patient["preferred_language"],
            "caregiver_id": str(patient["caregiver_id"]),
            "created_at": patient["created_at"].isoformat()
        })

    return {
        "status": "success",
        "count": len(patient_list),
        "patients": patient_list
    }, 200