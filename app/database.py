from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

# SQLALCHEMY_DATABASE_URI = "sqlite:///fastapi.db"
# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://my_user:my_password@127.0.0.1:5432/my_db"
# postgresql+psycopg2://user:passsowrd@host:5432/db_name

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# python type alias
Base = declarative_base()
