from flask import Blueprint, request, g

from app.middleware.auth_middleware import token_required
from app.models.patient_model import find_patient_by_id

from app.models.memory_model import (
    find_memories_by_patient,
    find_memory_by_id,
    delete_memory
)

from app.services.memory_service import create_patient_memory


memory_bp = Blueprint("memory", __name__)


# ==========================================
# CREATE MEMORY
# ==========================================

@memory_bp.route("/", methods=["POST"])
@token_required
def create():

    if g.user["role"] != "caregiver":
        return {
            "status": "error",
            "message": "Only caregivers can create memories"
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
        "description",
        "category"
    ]

    if not all(field in data for field in required_fields):
        return {
            "status": "error",
            "message": "All memory fields are required"
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

    result, error = create_patient_memory(
        patient_id=data["patient_id"],
        title=data["title"],
        description=data["description"],
        category=data["category"],
        image_url=data.get("image_url")
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 400

    return {
        "status": "success",
        "message": "Memory created successfully",
        "memory": result
    }, 201


# ==========================================
# GET PATIENT MEMORIES
# ==========================================

@memory_bp.route("/<patient_id>", methods=["GET"])
@token_required
def get_memories(patient_id):

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

    memories = find_memories_by_patient(patient_id)

    memory_list = []

    for memory in memories:
        memory_list.append({
            "id": str(memory["_id"]),
            "patient_id": str(memory["patient_id"]),
            "title": memory["title"],
            "description": memory["description"],
            "category": memory["category"],
            "image_url": memory.get("image_url"),
            "created_at": memory["created_at"].isoformat()
        })

    return {
        "status": "success",
        "count": len(memory_list),
        "memories": memory_list
    }, 200


# ==========================================
# DELETE MEMORY
# ==========================================

@memory_bp.route("/<memory_id>", methods=["DELETE"])
@token_required
def remove_memory(memory_id):

    memory = find_memory_by_id(memory_id)

    if not memory:
        return {
            "status": "error",
            "message": "Memory not found"
        }, 404

    patient = find_patient_by_id(
        str(memory["patient_id"])
    )

    if not patient:
        return {
            "status": "error",
            "message": "Patient not found"
        }, 404

    if str(patient["caregiver_id"]) != g.user["user_id"]:
        return {
            "status": "error",
            "message": "You are not authorized to delete this memory"
        }, 403

    deleted = delete_memory(memory_id)

    if not deleted:
        return {
            "status": "error",
            "message": "Memory could not be deleted"
        }, 400

    return {
        "status": "success",
        "message": "Memory deleted successfully"
    }, 200