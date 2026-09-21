from flask import Blueprint, request

from app.services.auth_service import (
    register_user,
    login_user
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([name, email, password, role]):
        return {
            "status": "error",
            "message": "Name, email, password and role are required"
        }, 400

    user_id, error = register_user(
        name=name,
        email=email,
        password=password,
        role=role
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 400

    return {
        "status": "success",
        "message": "User registered successfully",
        "user_id": user_id
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {
            "status": "error",
            "message": "Request body is required"
        }, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "status": "error",
            "message": "Email and password are required"
        }, 400

    result, error = login_user(
        email=email,
        password=password
    )

    if error:
        return {
            "status": "error",
            "message": error
        }, 401

    return {
        "status": "success",
        "message": "Login successful",
        "token": result["token"],
        "user": result["user"]
    }, 200