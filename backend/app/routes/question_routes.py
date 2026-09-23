import os
import jwt
from flask import Blueprint, request

from app.models.question_model import get_general_questions
from app.models.patient_model import find_patient_by_id, find_patient_by_user_id
from app.services.personalization_service import (
    patient_has_personal_info,
    generate_personalized_questions
)


question_bp = Blueprint("question", __name__)


# ==========================================
# GET QUESTIONS (Personalized if user provided info, else Backup)
# ==========================================

@question_bp.route("/general", methods=["GET"])
@question_bp.route("/quiz", methods=["GET"])
@question_bp.route("/", methods=["GET"])
def get_questions():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty", "easy")
    patient_id = request.args.get("patient_id")

    patient = None

    # 1. Resolve patient from query parameter if provided
    if patient_id:
        patient = find_patient_by_id(patient_id)
        if not patient:
            patient = find_patient_by_user_id(patient_id)

    # 2. If no patient_id param, inspect Bearer auth token if present
    if not patient:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            secret_key = os.getenv("JWT_SECRET_KEY")
            if secret_key:
                try:
                    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
                    user_id = payload.get("user_id")
                    if payload.get("role") == "patient":
                        patient = find_patient_by_user_id(user_id)
                except Exception:
                    pass

    # 3. If patient has provided personal info, generate personalized questions
    if patient and patient_has_personal_info(patient):
        try:
            personalized_qs = generate_personalized_questions(
                patient_data=patient,
                difficulty=difficulty,
                count=5
            )
            if personalized_qs and len(personalized_qs) > 0:
                return {
                    "status": "success",
                    "source": "personalized",
                    "patient_name": patient.get("preferred_name") or patient.get("name") or "Friend",
                    "count": len(personalized_qs),
                    "questions": personalized_qs
                }, 200
        except Exception as e:
            print("[SmritiRoots Questions] Personalization error, falling back to backup questions:", e)

    # 4. Fallback: Fixed set of backup questions
    questions = get_general_questions(
        category=category,
        difficulty=difficulty
    )

    safe_questions = []
    for question in questions:
        safe_questions.append({
            "id": question["id"],
            "category": question["category"],
            "difficulty": question["difficulty"],
            "question": question["question"],
            "options": question["options"],
            "answer": question.get("answer")
        })

    return {
        "status": "success",
        "source": "backup",
        "count": len(safe_questions),
        "questions": safe_questions
    }, 200