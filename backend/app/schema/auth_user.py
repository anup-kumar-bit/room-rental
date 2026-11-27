from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from typing import Optional


# ========================== REQUEST SCHEMA ==============================
# ----  User Schema ----
class UserBaseSchema(BaseModel):
    user_name: str
    email: EmailStr
    phone: str = Field(min_length=8, max_length=13)


# ---- Signup Payload  ----
class SignUpSchema(UserBaseSchema):
    password: str = Field(min_length=8)
    role_id: int = Field(gt=-1)


# ---- Login Payload ----
class LoginSchema(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def validateEmail_or_phone(self):
        if not self.email and not self.phone:
            raise ValueError("Either Email or Phone is Mandatory")
        return self


# ========================== RESPONSE SCHEMA ==============================
# ----  User Data Back  ----
class UserResponse(UserBaseSchema):
    id: UUID
    role_id: int
    status: bool

    model_config = ConfigDict(from_attributes=True)
