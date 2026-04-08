from app.db.base import Base
from app.db.session import engine

print("Registered tables:")
print(Base.metadata.tables.keys())

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
