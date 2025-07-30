from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from tech_challenge1.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

# Para SQLite precisa desse flag, em outros DBs basta omitir connect_args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()