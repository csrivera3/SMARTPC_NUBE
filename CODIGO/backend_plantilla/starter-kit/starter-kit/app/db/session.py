import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = settings.DATABASE_URL
logger.info(f"Initializing database connection: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "client_encoding": "utf8",
        "connect_timeout": 10,
    },
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections every hour
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
