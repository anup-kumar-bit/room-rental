from fastapi.responses import JSONResponse
from sqlalchemy import or_

from app.utils.config import settings

# -----Models----
from app.models.auth_user_model import User
from app.models.dropdown_model import UserRole

# -----Helper Funtion-----
from app.utils.security import hashPassword, create_access_token, checkpassword

# -----Response Schema -----
from app.schema.auth_user import UserResponse

MAX_AGE = settings.jwt_expirein * 60
ADMIN_ROLE = 0


def signup(req, res, db):
    try:
        user = (
            db.query(User)
            .filter(or_(User.email == req.email, User.phone == req.phone))
            .first()
        )

        if user:
            return JSONResponse(
                status_code=409,
                content={"message": "User already exists", "data": None},
            )

        role = db.query(UserRole).filter(UserRole.id == req.role_id).first()

        if not role or req.role_id == ADMIN_ROLE:
            return JSONResponse(
                status_code=400, content={"message": "Invalid Role", "data": None}
            )

        new_user = User(
            user_name=req.user_name,
            email=req.email,
            phone=req.phone,
            password_hash=hashPassword(req.password),
            role_id=req.role_id,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token(str(new_user.id))
        data = UserResponse.model_validate(new_user).model_dump(mode="json")

        response = JSONResponse(
            status_code=201, content={"message": "Signup successful", "data": data}
        )

        response.set_cookie(
            key="access_token",
            value=token,
            max_age=MAX_AGE,
            httponly=True,
            samesite="lax",
            secure=False,
        )
        return response

    except Exception as e:
        db.rollback()
        print("Error:", e)
        return JSONResponse(
            status_code=500, content={"message": "Internal server error", "data": None}
        )


def login(req, res, db):
    try:
        user = None
        if req.email:
            user = db.query(User).filter(User.email == req.email).first()
        else:
            user = db.query(User).filter(User.phone == req.phone).first()

        if not user:
            return JSONResponse(
                status_code=401, content={"message": "Invalid Credential", "data": None}
            )

        validate_password = checkpassword(req.password, user.password_hash)

        if not validate_password:
            return JSONResponse(
                status_code=401, content={"message": "Invalid Credential", "data": None}
            )

        if not user.status:
            return JSONResponse(
                status_code=403,
                content={"message": "Account does not Exist", "data": None},
            )

        token = create_access_token(str(user.id))

        data = UserResponse.model_validate(user).model_dump(mode="json")

        response = JSONResponse(
            status_code=200,
            content={"message": "User logged in Successfully", "data": data},
        )

        response.set_cookie(
            key="access_token",
            value=token,
            max_age=MAX_AGE,
            httponly=True,
            samesite="lax",
            secure=False,
        )

        return response

    except Exception as e:
        print(f"Login Error: {str(e)}")

        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error", "data": None}
        )
