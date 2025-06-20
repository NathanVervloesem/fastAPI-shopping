from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Use SQLite for local dev or PostgreSQL on Render
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# For Postgres, use something like:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)