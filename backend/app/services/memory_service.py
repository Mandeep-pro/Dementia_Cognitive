from app.models.memory_model import create_memory


ALLOWED_CATEGORIES = [
    "family",
    "place",
    "person",
    "object",
    "event",
    "other"
]


def create_patient_memory(
    patient_id,
    title,
    description,
    category,
    image_url=None
):

    if category not in ALLOWED_CATEGORIES:
        return None, "Invalid memory category"

    if not title.strip():
        return None, "Memory title is required"

    if not description.strip():
        return None, "Memory description is required"

    memory_id = create_memory(
        patient_id=patient_id,
        title=title.strip(),
        description=description.strip(),
        category=category,
        image_url=image_url
    )

    return {
        "id": memory_id,
        "memory_id": memory_id
    }, None