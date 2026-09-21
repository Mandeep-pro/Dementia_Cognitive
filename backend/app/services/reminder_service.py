from app.models.reminder_model import create_reminder


ALLOWED_CATEGORIES = [
    "medicine",
    "hydration",
    "activity",
    "appointment",
    "other"
]


def create_patient_reminder(
    patient_id,
    title,
    category,
    scheduled_time
):

    if category not in ALLOWED_CATEGORIES:
        return None, "Invalid reminder category"

    if not title.strip():
        return None, "Reminder title is required"

    if not scheduled_time.strip():
        return None, "Scheduled time is required"

    reminder_id = create_reminder(
        patient_id=patient_id,
        title=title.strip(),
        category=category,
        scheduled_time=scheduled_time.strip()
    )

    return {
        "reminder_id": reminder_id
    }, None