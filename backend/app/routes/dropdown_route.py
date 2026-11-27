from fastapi import APIRouter, Depends, Response

from app.controllers.dropdowns import user_roles
from app.schema.dropdowns import CreateRoleRequest
from app.utils.database import get_db
from app.utils.dependencies import require_admin

dropdownRouter = APIRouter(prefix="/api/dropdowns", tags=["Dropdowns"])


@dropdownRouter.post("/roles", dependencies=[Depends(require_admin)])
def add_role(request: CreateRoleRequest, response: Response, db=Depends(get_db)):
    return user_roles.add_new_role(request, response, db)
