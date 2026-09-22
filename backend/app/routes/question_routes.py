from flask import Blueprint, request

from app.models.question_model import get_general_questions


question_bp = Blueprint("question", __name__)


# ==========================================
# GET GENERAL QUESTIONS
# ==========================================

@question_bp.route("/general", methods=["GET"])
def get_questions():

    category = request.args.get("category")
    difficulty = request.args.get("difficulty")

    questions = get_general_questions(
        category=category,
        difficulty=difficulty
    )

    # Never send the correct answer to the patient
    safe_questions = []

    for question in questions:
        safe_questions.append({
            "id": question["id"],
            "category": question["category"],
            "difficulty": question["difficulty"],
            "question": question["question"],
            "options": question["options"]
        })

    return {
        "status": "success",
        "count": len(safe_questions),
        "questions": safe_questions
    }, 200