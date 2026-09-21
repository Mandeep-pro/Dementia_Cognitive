import bcrypt

from app.models.user_model import (
    create_user,
    find_user_by_email
)

from app.models.patient_model import create_patient


def create_patient_for_caregiver(
    name,
    email,
    password,
    preferred_name,
    age,
    preferred_language,
    caregiver_id
):
    # Check if the email is already registered
    existing_user = find_user_by_email(email)

    if existing_user:
        return None, "Email already registered"

    # Hash patient password
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create patient login account
    user_id = create_user(
        name=name,
        email=email,
        password_hash=password_hash,
        role="patient"
    )

    # Create patient profile
    patient_id = create_patient(
        user_id=user_id,
        preferred_name=preferred_name,
        age=age,
        preferred_language=preferred_language,
        caregiver_id=caregiver_id
    )

    return {
        "user_id": user_id,
        "patient_id": patient_id
    }, None