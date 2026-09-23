import re

def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email.strip()) is not None

def is_valid_password(password, min_length=6):
    if not password or not isinstance(password, str):
        return False
    return len(password) >= min_length
