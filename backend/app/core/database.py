from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

from app.core.config import settings

# DATABASE_URL = (
#     f"postgresql://"
#     f"{settings.DB_USER}:"
#     f"{settings.DB_PASSWORD}@"
#     f"{settings.DB_HOST}:"
#     f"{settings.DB_PORT}/"
#     f"{settings.DB_NAME}"
# )


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_engine(DATABASE_URL,echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind = engine
)

base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

