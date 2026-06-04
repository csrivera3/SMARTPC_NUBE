import os
import psycopg2
from psycopg2 import sql
from app.db.base import Base
from app.db.session import engine
from urllib.parse import urlparse

# Parse DATABASE_URL to extract connection details
database_url = os.getenv("DATABASE_URL", "")
if not database_url:
    print("ERROR: DATABASE_URL environment variable is not set!")
    print("Set DATABASE_URL to your PostgreSQL connection string (from Railway or local DB)")
    exit(1)

parsed_url = urlparse(database_url)
db_user = parsed_url.username or os.getenv("DB_USER", "postgres")
db_password = parsed_url.password or os.getenv("DB_PASSWORD", "")
db_host = parsed_url.hostname or os.getenv("DB_HOST", "localhost")
db_port = parsed_url.port or int(os.getenv("DB_PORT", 5432))
db_name = parsed_url.path.lstrip("/") or os.getenv("DB_NAME", "mesa_db")

# First, create the database if it doesn't exist
try:
    # Connect to default 'postgres' database to create our database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), [db_name])
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name)))
        print(f"✓ Database '{db_name}' created successfully")
    else:
        print(f"✓ Database '{db_name}' already exists")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")
    print("Note: This is normal if DATABASE_URL points to a managed database (like Railway)")
    print("The database should already exist in that case.")

# Now create all tables using the configured engine
try:
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")
