from fastapi import APIRouter, Response, Depends

from app.schema.auth_user import SignUpSchema
from app.utils.database import get_db
from app.controllers import auth

authRouter = APIRouter(prefix="/api/auth", tags=["Authentication"])


@authRouter.post("/signup")
def signup(request: SignUpSchema, response: Response, db=Depends(get_db)):
    print("REQUEST", request)
    return auth.signup(request,response,db)
