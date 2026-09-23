import os
import jwt
from functools import wraps
from flask import request, g


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {
                "status": "error",
                "message": "Authorization header is required"
            }, 401

        if not auth_header.startswith("Bearer "):
            return {
                "status": "error",
                "message": "Invalid authorization format"
            }, 401

        token = auth_header.split(" ", 1)[1]

        secret_key = os.getenv("JWT_SECRET_KEY")

        if not secret_key:
            return {
                "status": "error",
                "message": "JWT secret key is not configured"
            }, 500

        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=["HS256"]
            )

            # Store logged-in user's information
            # so routes can access it.
            g.user = payload

        except jwt.ExpiredSignatureError:
            return {
                "status": "error",
                "message": "Token has expired"
            }, 401

        except jwt.InvalidTokenError:
            return {
                "status": "error",
                "message": "Invalid token"
            }, 401

        return f(*args, **kwargs)

    return decorated