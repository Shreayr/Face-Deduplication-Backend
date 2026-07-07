from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:shreya2439@localhost:5432/deduplication_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, #Don't save changes automatically. Wait until I explicitly call db.commit().
    autoflush=False,#will not automatically flush pending changes
    bind=engine
)

Base = declarative_base()#creates a special base class.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()