# Import every model module here so SQLAlchemy and Alembic can see all tables.
# When you add a new model file, add an import for it here too.
from app.models.dropdown_model import UserRole
from app.models.auth_user_model import User
