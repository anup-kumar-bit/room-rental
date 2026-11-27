from sqlalchemy import Column, Integer, String, Boolean, text

from app.utils.database import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)
    status = Column(Boolean, nullable=False, default=True, server_default=text("true"))
