import jwt
import hashlib
import re
from datetime import datetime, timedelta
from config import SECRET_KEY, JWT_EXPIRATION
from database import get_db_connection

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one capital letter"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, ""

def validate_username(username):
    if ' ' in username:
        return False, "Username cannot contain spaces"
    return True, ""

def validate_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        return False, "Invalid email format"
    return True, ""

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id):
    expiration = datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
    return jwt.encode(
        {'user_id': user_id, 'exp': expiration},
        SECRET_KEY,
        algorithm='HS256'
    )

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(username, email, password):
    # Validate username, email and password
    username_valid, username_error = validate_username(username)
    if not username_valid:
        raise ValueError(username_error)
    
    email_valid, email_error = validate_email(email)
    if not email_valid:
        raise ValueError(email_error)
    
    password_valid, password_error = validate_password(password)
    if not password_valid:
        raise ValueError(password_error)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = %s AND password = %s",
            (username, hashed_password)
        )
        user = cursor.fetchone()
        if user:
            token = generate_token(user['id'])
            return {'user': user, 'token': token}
        return None
    finally:
        cursor.close()
        conn.close()
