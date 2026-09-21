from flask import Blueprint, request, g

from app.middleware.auth_middleware import token_required
from app.models.patient_model import find_patient_by_id

from app.models.reminder_model import (
    find_reminders_by_patient,
    find_reminder_by_id,
    update_reminder_status,
    delete_reminder
)

from app.services.reminder_service import create_patient_reminder


reminder_bp = Blueprint("reminder", __name__)


# ==========================================
# CREATE REMINDER
# ==========================================

@reminder_bp.route("/", methods=["POST"])
@token_required
def create():

    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can create reminders"
        }, 403

    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    required_fields = [
        "patient_id",
        "title",
        "category",
        "scheduled_time"
    ]

    if not all(field in data for field in required_fields):
        return {
            "status": "error",
            "message": "All reminder fields are required"
        }, 400

    patient = find_patient_by_id(data["patient_id"])

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

    result, error = create_patient_reminder(
        patient_id=data["patient_id"],
        title=data["title"],
        category=data["category"],
        scheduled_time=data["scheduled_time"]
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 400

    return {
        "status": "success",
        "message": "Reminder created successfully",
        "reminder": result
    }, 201


# ==========================================
# GET PATIENT REMINDERS
# ==========================================

@reminder_bp.route("/<patient_id>", methods=["GET"])
@token_required
def get_reminders(patient_id):

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

    reminders = find_reminders_by_patient(patient_id)

    reminder_list = []

    for reminder in reminders:
        reminder_list.append({
            "id": str(reminder["_id"]),
            "patient_id": str(reminder["patient_id"]),
            "title": reminder["title"],
            "category": reminder["category"],
            "scheduled_time": reminder["scheduled_time"],
            "completed": reminder["completed"],
            "created_at": reminder["created_at"].isoformat()
        })

    return {
        "status": "success",
        "count": len(reminder_list),
        "reminders": reminder_list
    }, 200


    # ==========================================
# MARK REMINDER AS COMPLETED
# ==========================================

@reminder_bp.route("/<reminder_id>/complete", methods=["PUT"])
@token_required
def complete_reminder(reminder_id):

    reminder = find_reminder_by_id(reminder_id)

    if not reminder:
        return {
            "status": "error",
            "message": "Reminder not found"
        }, 404

    patient = find_patient_by_id(
        str(reminder["patient_id"])
    )

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized for this reminder"
        }, 403

    updated = update_reminder_status(
        reminder_id,
        True
    )

    if not updated:
        return {
            "status": "error",
            "message": "Reminder could not be updated"
        }, 400

    return {
        "status": "success",
        "message": "Reminder marked as completed"
    }, 200


# ==========================================
# DELETE REMINDER
# ==========================================

@reminder_bp.route("/<reminder_id>", methods=["DELETE"])
@token_required
def remove_reminder(reminder_id):

    reminder = find_reminder_by_id(reminder_id)

    if not reminder:
        return {
            "status": "error",
            "message": "Reminder not found"
        }, 404

    patient = find_patient_by_id(
        str(reminder["patient_id"])
    )

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized to delete this reminder"
        }, 403

    deleted = delete_reminder(reminder_id)

    if not deleted:
        return {
            "status": "error",
            "message": "Reminder could not be deleted"
        }, 400

    return {
        "status": "success",
        "message": "Reminder deleted successfully"
    }, 200