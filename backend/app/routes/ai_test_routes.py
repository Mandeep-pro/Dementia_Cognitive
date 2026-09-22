from flask import Blueprint

from app.services.personalization_service import generate_personalized_questions

ai_test_bp = Blueprint("ai_test", __name__)


@ai_test_bp.route("/test", methods=["GET"])
def test_gemini():

    patient_data = {
        "preferred_name": "Grandma",
        "family": ["daughter", "son"],
        "favorite_things": ["tea", "gardening"],
        "daily_routine": ["morning tea", "watering plants"],
        "important_places": ["home garden"],
        "personal_memories": [
            "Enjoys spending time in the garden"
        ]
    }

    try:
        questions = generate_personalized_questions(
            patient_data=patient_data,
            difficulty="easy",
            count=3
        )

        return {
            "status": "success",
            "questions": questions
        }, 200

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500