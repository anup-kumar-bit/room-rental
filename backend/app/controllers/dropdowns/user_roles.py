from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.models.dropdown_model import UserRole
from app.schema.dropdowns import AdminRoleResponse


def nametaken(name, db, exclude_id=None):
    query = db.query(UserRole).filter(func.lower(UserRole.role_name) == name.lower())
    if exclude_id is not None:
        query = query.filter(UserRole.id != exclude_id)
    return query.first() is not None


def add_new_role(req, res, db):
    role_name = req.role_name.strip()

    if not role_name:
        return JSONResponse(
            status_code=400,
            content={"message": "Role name is required", "data": None},
        )

    try:
        if nametaken(role_name, db):
            return JSONResponse(
                status_code=409,
                content={"message": "Role name already taken", "data": None},
            )

        new_role = UserRole(role_name=role_name)

        db.add(new_role)
        db.commit()
        db.refresh(new_role)

        data = AdminRoleResponse.model_validate(new_role).model_dump()
        return JSONResponse(
            status_code=201,
            content={"message": "Role created Successfully", "data": data},
        )

    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=409,
            content={"message": "Role name already taken", "data": None},
        )

    except Exception as e:
        db.rollback()
        print("Getting error in adding role", e)
        return JSONResponse(
            status_code=500, content={"message": "Internal Server error", "data": None}
        )


def update_role(req, res, db):
    pass
