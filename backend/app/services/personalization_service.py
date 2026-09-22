import os
import json
from google import genai


def generate_personalized_questions(
    patient_data,
    difficulty="easy",
    count=5
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    personal_context = {
        "preferred_name": patient_data.get("preferred_name"),
        "family": patient_data.get("family", []),
        "favorite_things": patient_data.get("favorite_things", []),
        "daily_routine": patient_data.get("daily_routine", []),
        "important_places": patient_data.get("important_places", []),
        "personal_memories": patient_data.get("personal_memories", [])
    }

    prompt = f"""
Create {count} simple multiple-choice cognitive engagement
questions for an elderly person.

Difficulty: {difficulty}

Use the person's information to make questions familiar
and meaningful.

Rules:
- Keep questions simple and respectful.
- Exactly 4 options per question.
- Exactly 1 correct answer.
- Do not create medical or diagnostic questions.
- Use only the information provided.
- Do not invent personal facts.

Patient information:
{json.dumps(personal_context, default=str)}

Return ONLY valid JSON:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
            ],
            "answer": "Correct option",
            "category": "memory",
            "difficulty": "{difficulty}"
        }}
    ]
}}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    text = interaction.output_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    return result["questions"]