from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# A sua URL mágica do PostgreSQL na nuvem (Render)
SQLALCHEMY_DATABASE_URL = "postgresql://sentinela_db_wp51_user:COkMKd5UttRbCrEluyqRhI9tY6WdJ3ip@dpg-d7t8vmreo5us73ft1udg-a.oregon-postgres.render.com/sentinela_db_wp51"

# O PostgreSQL não precisa daquele argumento "check_same_thread" que o SQLite usava
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()