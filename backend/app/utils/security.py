import jwt
import bcrypt

from datetime import datetime, timezone, timedelta
from app.utils.config import settings


def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf")


def checkpassword(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))


def create_access_token(information: str):
    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expirein)
    payload = {"sub": information, "exp": expiry}
    return jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)
