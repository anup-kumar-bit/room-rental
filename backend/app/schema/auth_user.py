from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ========================== REQUEST SCHEMA ==============================
# ----  User Schema ----
class UserBaseSchema(BaseModel):
    user_name: str
    email: EmailStr
    phone: str = Field(min_length=8, max_length=13)


# ---- Signup Payload  ----
class SignUpSchema(UserBaseSchema):
    password: str = Field(min_length=8)
    role_id: int = Field(gt=0)


# ========================== RESPONSE SCHEMA ==============================
# ----  User Data Back  ----
class UserResponse(UserBaseSchema):
    id: UUID
    role_id: int
    status: bool

    model_config = ConfigDict(from_attributes=True)
