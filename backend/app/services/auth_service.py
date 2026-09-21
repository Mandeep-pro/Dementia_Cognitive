import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone

from app.models.user_model import (
    create_user,
    find_user_by_email
)


ALLOWED_ROLES = ["patient", "caregiver"]


def register_user(name, email, password, role):
    if role not in ALLOWED_ROLES:
        return None, "Invalid role"

    existing_user = find_user_by_email(email)

    if existing_user:
        return None, "Email already registered"

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user_id = create_user(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role
    )

    return user_id, None


def login_user(email, password):
    user = find_user_by_email(email)

    if not user:
        return None, "Invalid email or password"

    password_matches = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )

    if not password_matches:
        return None, "Invalid email or password"

    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        return None, "JWT secret key is not configured"

    payload = {
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }, None