GAMES = [
    {
        "id": "brain-boost",
        "name": "Brain Boost Quiz",
        "description": "Gentle question and answer puzzles to keep your mind sharp and active.",
        "category": "memory",
        "default_difficulty": "easy"
    },
    {
        "id": "memory-match",
        "name": "Memory Match",
        "description": "Match the same objects to exercise memory.",
        "category": "memory",
        "default_difficulty": "easy"
    },
    {
        "id": "attention-focus",
        "name": "Attention Focus",
        "description": "Find the correct object and improve concentration.",
        "category": "attention",
        "default_difficulty": "easy"
    },
    {
        "id": "pattern-recognition",
        "name": "Pattern Recognition",
        "description": "Identify the missing object in a simple pattern.",
        "category": "pattern",
        "default_difficulty": "easy"
    },
    {
        "id": "daily-routine",
        "name": "Daily Routine Recall",
        "description": "Recall common daily activities in the correct order.",
        "category": "routine",
        "default_difficulty": "easy"
    }
]


def get_all_games():
    return GAMES


def get_game_by_id(game_id):
    if not game_id:
        return None
    for game in GAMES:
        if game["id"] == game_id:
            return game

    # Graceful fallback for custom or dynamic quizzes
    return {
        "id": game_id,
        "name": game_id.replace("-", " ").title(),
        "description": "Cognitive workout game",
        "category": "memory",
        "default_difficulty": "easy"
    }