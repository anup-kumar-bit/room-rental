from fastapi import APIRouter, Response, Depends

from app.schema.auth_user import SignUpSchema, LoginSchema
from app.utils.database import get_db
from app.controllers import auth

authRouter = APIRouter(prefix="/api/auth", tags=["Authentication"])


@authRouter.post("/signup")
def signup(request: SignUpSchema, response: Response, db=Depends(get_db)):
    # print("SIGNUP REQUEST", request)
    return auth.signup(request, response, db)


@authRouter.post("/login")
def login(request: LoginSchema, response: Response, db=Depends(get_db)):
    # print("LOGIN REQUEST", request)
    return auth.login(request, response, db)
