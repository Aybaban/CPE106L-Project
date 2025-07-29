"""
SQLAlchemy Database Setup
This module handles the connection to the SQLite database using SQLAlchemy.
It provides the engine, sessionmaker, and a dependency for FastAPI to get a database session.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variables
# Default to a local SQLite database file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite
# to allow multiple threads to interact with the database connection.
# This is a common requirement for FastAPI applications using SQLite.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class
# Each instance of SessionLocal will be a database session.
# The 'autocommit=False' means that the session will not commit changes
# automatically. You'll need to explicitly call session.commit().
# The 'autoflush=False' means that objects will not be flushed to the database
# until commit or query.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency for FastAPI to get a database session.
    This function will be used with `Depends` in FastAPI route functions.
    It ensures that the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models to ensure they are registered with SQLAlchemy Base
# This is crucial for Base.metadata.create_all(engine) to work correctly
from backend.app import models
def init_db():
    """
    Initializes the database by creating all tables defined in models.
    This function should be called on application startup.
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created (or already exist).")

```python
