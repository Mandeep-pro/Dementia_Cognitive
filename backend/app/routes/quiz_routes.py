from flask import Blueprint, request

from app.models.question_model import GENERAL_QUESTIONS


quiz_bp = Blueprint("quiz", __name__)


# ==========================================
# CHECK ANSWER
# ==========================================

@quiz_bp.route("/check-answer", methods=["POST"])
def check_answer():

    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    question_id = data.get("question_id")
    selected_answer = data.get("selected_answer")

    if not question_id or selected_answer is None:
        return {
            "status": "error",
            "message": "question_id and selected_answer are required"
        }, 400

    question = next(
        (
            q for q in GENERAL_QUESTIONS
            if q["id"] == question_id
        ),
        None
    )

    if not question:
        return {
            "status": "error",
            "message": "Question not found"
        }, 404

    is_correct = selected_answer == question["answer"]

    return {
        "status": "success",
        "correct": is_correct
    }, 200