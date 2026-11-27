import uuid

import jwt
from fastapi import Depends, HTTPException, Request

from app.models.auth_user_model import User
from app.utils.config import settings
from app.utils.database import get_db

ADMIN_ROLE = 0


def get_current_user(request: Request, db=Depends(get_db)) -> User:
    """Login wala user: access_token cookie se JWT padho aur user load karo."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.status:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    """Sirf Admin role (id 0) wale users aage ja sakte hain."""
    if user.role_id != ADMIN_ROLE:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
