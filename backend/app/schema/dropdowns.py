from pydantic import BaseModel, ConfigDict


# ========================== REQUEST SCHEMA ==============================
# ---- Admin Based ROLE ----
class AdminRole(BaseModel):
    id: int
    role_name: str


# ========================== REQUEST SCHEMA ==============================
class AdminRoleResponse(BaseModel):
    id: int
    role_name: str
    status: bool

    model_config = ConfigDict(from_attributes=True)
