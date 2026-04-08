from app.db.base import Base
from app.db.session import engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
