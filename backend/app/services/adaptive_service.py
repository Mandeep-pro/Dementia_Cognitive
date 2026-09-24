from collections import Counter

from app.config.database import db


DIFFICULTY_LEVELS = [
    "easy",
    "medium",
    "hard"
]

DIFFICULTY_TO_NUMBER = {
    difficulty: index
    for index, difficulty in enumerate(DIFFICULTY_LEVELS)
}

game_results_collection = db["game_results"]


def _rule_based_difficulty(current_difficulty, accuracy):
    """Conservative fallback used before enough training data exists."""
    if current_difficulty not in DIFFICULTY_LEVELS:
        current_difficulty = DIFFICULTY_LEVELS[0]

    current_index = DIFFICULTY_LEVELS.index(current_difficulty)

    if accuracy >= 80 and current_index < len(DIFFICULTY_LEVELS) - 1:
        return DIFFICULTY_LEVELS[current_index + 1]

    if accuracy < 50 and current_index > 0:
        return DIFFICULTY_LEVELS[current_index - 1]

    return current_difficulty


def get_next_difficulty(current_difficulty, accuracy):
    return _rule_based_difficulty(current_difficulty, accuracy)


def _patient_features(patient):
    """Convert caregiver-provided profile data into stable numeric features."""
    stage = str(patient.get("cognitive_stage", "unknown")).lower()
    stage_values = {"unknown": 0, "mild": 1, "moderate": 2, "severe": 3}

    try:
        age = float(patient.get("age") or 0)
    except (TypeError, ValueError):
        age = 0

    return age, stage_values.get(stage, 0)


def _result_features(result, patient):
    current_difficulty = result.get("difficulty", "easy")
    try:
        accuracy = float(result.get("accuracy", 0))
    except (TypeError, ValueError):
        accuracy = 0

    try:
        time_taken = float(result.get("time_taken", 0))
    except (TypeError, ValueError):
        time_taken = 0

    age, cognitive_stage = _patient_features(patient)
    return [
        DIFFICULTY_TO_NUMBER.get(current_difficulty, 0),
        accuracy,
        time_taken,
        age,
        cognitive_stage
    ]


def recommend_next_difficulty(patient, current_difficulty, accuracy, time_taken=0):
    """Predict the next difficulty using MongoDB history and XGBoost.

    The target is deliberately limited to one adjacent difficulty level. This
    prevents a model prediction from abruptly changing the patient's session.
    """
    fallback = _rule_based_difficulty(current_difficulty, accuracy)
    patient_id = patient.get("_id") if patient else None

    if not patient_id:
        return fallback, "rule_based", 0

    try:
        results = list(
            game_results_collection.find({"patient_id": {"$in": [patient_id, str(patient_id)]}})
            .sort("created_at", 1)
        )
    except Exception as error:
        print("Adaptive model history lookup failed:", error)
        return fallback, "rule_based", 0

    # XGBoost needs multiple target classes. The rule remains the safe bootstrap.
    if len(results) < 10:
        return fallback, "rule_based", len(results)

    training_results = [
        result for result in results
        if result.get("difficulty", "easy") in DIFFICULTY_TO_NUMBER
    ]
    labels = [
        DIFFICULTY_TO_NUMBER[_rule_based_difficulty(
            result.get("difficulty", "easy"),
            float(result.get("accuracy", 0) or 0)
        )]
        for result in training_results
    ]

    unique_labels = sorted(set(labels))
    if len(labels) < 10 or len(unique_labels) < 2:
        return fallback, "rule_based", len(labels)

    try:
        from xgboost import XGBClassifier

        label_to_class = {
            label: class_number
            for class_number, label in enumerate(unique_labels)
        }
        training_labels = [label_to_class[label] for label in labels]
        features = [
            _result_features(result, patient)
            for result in training_results
        ]
        current_result = {
            "difficulty": current_difficulty,
            "accuracy": accuracy,
            "time_taken": time_taken
        }

        model = XGBClassifier(
            n_estimators=60,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="multi:softprob",
            eval_metric="mlogloss",
            num_class=len(unique_labels),
            random_state=42,
            n_jobs=1
        )
        model.fit(features, training_labels)
        predicted_class = int(model.predict([_result_features(current_result, patient)])[0])
        predicted_number = unique_labels[predicted_class]
        predicted_number = max(0, min(predicted_number, len(DIFFICULTY_LEVELS) - 1))

        current_number = DIFFICULTY_TO_NUMBER.get(current_difficulty, 0)
        predicted_number = max(current_number - 1, min(current_number + 1, predicted_number))
        confidence = float(max(model.predict_proba([_result_features(current_result, patient)])[0]))

        return DIFFICULTY_LEVELS[predicted_number], "xgboost", round(confidence, 3)
    except Exception as error:
        print("Adaptive XGBoost prediction failed:", error)
        return fallback, "rule_based", len(labels)