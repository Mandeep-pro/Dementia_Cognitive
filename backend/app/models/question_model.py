GENERAL_QUESTIONS = [
    {
        "id": "q1",
        "category": "memory",
        "difficulty": "easy",
        "question": "Which fruit is usually yellow?",
        "options": [
            "Apple",
            "Banana",
            "Grape",
            "Orange"
        ],
        "answer": "Banana"
    },
    {
        "id": "q2",
        "category": "memory",
        "difficulty": "easy",
        "question": "Which animal is known for saying 'meow'?",
        "options": [
            "Dog",
            "Cow",
            "Cat",
            "Horse"
        ],
        "answer": "Cat"
    },
    {
        "id": "q3",
        "category": "attention",
        "difficulty": "easy",
        "question": "Which one is different from the others?",
        "options": [
            "Apple",
            "Banana",
            "Mango",
            "Car"
        ],
        "answer": "Car"
    },
    {
        "id": "q4",
        "category": "routine",
        "difficulty": "easy",
        "question": "What do people usually do after waking up?",
        "options": [
            "Go to sleep",
            "Get ready for the day",
            "Have dinner",
            "Go to bed"
        ],
        "answer": "Get ready for the day"
    },
    {
        "id": "q5",
        "category": "memory",
        "difficulty": "medium",
        "question": "Which item would most likely be found in a kitchen?",
        "options": [
            "Spoon",
            "Pillow",
            "Shoes",
            "Notebook"
        ],
        "answer": "Spoon"
    },
    {
        "id": "q6",
        "category": "attention",
        "difficulty": "medium",
        "question": "Which number comes next: 2, 4, 6, 8, ?",
        "options": [
            "9",
            "10",
            "11",
            "12"
        ],
        "answer": "10"
    }
]


def get_general_questions(category=None, difficulty=None):
    questions = GENERAL_QUESTIONS

    if category:
        questions = [
            q for q in questions
            if q["category"] == category
        ]

    if difficulty:
        questions = [
            q for q in questions
            if q["difficulty"] == difficulty
        ]

    return questions