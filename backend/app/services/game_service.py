from app.models.game_model import get_game_by_id
from app.models.game_result_model import create_game_result
from app.models.patient_model import find_patient_by_id


def save_game_result(
    patient_id,
    game_id,
    score,
    accuracy,
    time_taken,
    difficulty
):
    # Check that the patient exists
    patient = find_patient_by_id(patient_id)

    if not patient:
        return None, "Patient not found"

    # Check that the game exists
    game = get_game_by_id(game_id)

    if not game:
        return None, "Game not found"

    # Validate score
    if score < 0:
        return None, "Score cannot be negative"

    # Validate accuracy
    if accuracy < 0 or accuracy > 100:
        return None, "Accuracy must be between 0 and 100"

    # Validate time
    if time_taken < 0:
        return None, "Time taken cannot be negative"

    # Validate difficulty
    allowed_difficulties = [
        "easy",
        "medium",
        "hard"
    ]

    if difficulty not in allowed_difficulties:
        return None, "Invalid difficulty"

    result_id = create_game_result(
        patient_id=patient_id,
        game_id=game_id,
        score=score,
        accuracy=accuracy,
        time_taken=time_taken,
        difficulty=difficulty
    )

    return {
        "result_id": result_id
    }, None