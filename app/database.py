from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///fastapi.db"
SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
)
# postgresql+psycopg2://user:passsowrd@host:5432/db_name
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

# python type alias
Base = declarative_base()
