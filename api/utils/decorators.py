"""Decorators that decode and verify authorization tokens."""
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from api.models.users import User
from http import HTTPStatus

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user.is_admin:
            return {"message": "Admin permission required"}
        return fn(*args, **kwargs)
    return wrapper

def admin_or_current_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or not current_user.is_admin:
            return {"message": "Admin permission required"}
        return fn(*args, **kwargs)
    return wrapper