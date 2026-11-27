from pydantic import BaseModel, ConfigDict, Field


# ========================== REQUEST SCHEMA ==============================
# ---- Admin Based ROLE ----
class CreateRoleRequest(BaseModel):
    role_name: str = Field(min_length=1, max_length=50)


class AdminRole(BaseModel):
    id: int
    role_name: str = Field(min_length=1, max_length=50)


# ========================== RESPONSE SCHEMA ==============================
class AdminRoleResponse(BaseModel):
    id: int
    role_name: str
    status: bool

    model_config = ConfigDict(from_attributes=True)
