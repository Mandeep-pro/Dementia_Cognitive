DIFFICULTY_LEVELS = [
    "easy",
    "medium",
    "hard"
]


def get_next_difficulty(current_difficulty, accuracy):

    if current_difficulty not in DIFFICULTY_LEVELS:
        return "easy"

    if accuracy >= 80:
        current_index = DIFFICULTY_LEVELS.index(
            current_difficulty
        )

        if current_index < len(DIFFICULTY_LEVELS) - 1:
            return DIFFICULTY_LEVELS[current_index + 1]

        return current_difficulty

    if accuracy < 50:
        current_index = DIFFICULTY_LEVELS.index(
            current_difficulty
        )

        if current_index > 0:
            return DIFFICULTY_LEVELS[current_index - 1]

        return current_difficulty

    return current_difficulty