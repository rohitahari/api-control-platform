from app.db.base_class import Base
from app.db.session import engine

# import ALL models so SQLAlchemy knows them
from app.db.models.user import User
from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.api_key import ApiKey

Base.metadata.create_all(bind=engine)

print("Tables created successfully")
