GAMES = [
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
    for game in GAMES:
        if game["id"] == game_id:
            return game

    return None