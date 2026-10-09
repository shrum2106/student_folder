# Change line 1 from 'from config import settings' to:
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Grab the URL from your config settings
SQLALCHEMY_DATABASE_URL = settings.database_url

# 2. Create the engine connection for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} 
)

# 3. Create a session factory to handle transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class for database tables
Base = declarative_base()
# This forces SQLAlchemy to look at your Base tables and physically create the file
Base.metadata.create_all(bind=engine)
# Change line 20 from 'import app.model as model' to:
# Change line 22 from 'import model' to:
import app.model as model



