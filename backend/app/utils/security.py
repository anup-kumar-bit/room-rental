import jwt
import bcrypt


def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf")


def checkpassword(password: str, hash_password: str) -> str:
    return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))
