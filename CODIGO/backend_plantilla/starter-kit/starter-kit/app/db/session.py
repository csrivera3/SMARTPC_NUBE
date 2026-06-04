from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Use pool configuration appropriate for the environment
# - Development: Regular pool with connection recycling
# - Production/Railway: NullPool (no connection pooling, more reliable for serverless)
if settings.ENVIRONMENT == "production" or settings.ENVIRONMENT == "railway":
    # Railway doesn't work well with connection pooling
    pool_config = {
        "poolclass": NullPool,
    }
else:
    # Development environment uses regular pool
    pool_config = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 3600,  # Recycle connections after 1 hour
        "echo": settings.DEBUG,  # Log SQL queries in debug mode
    }

engine = create_engine(
    DATABASE_URL,
    connect_args={"client_encoding": "utf8", "connect_timeout": 10},
    **pool_config
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
