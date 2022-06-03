"""Create SQLAlchemy engine and session objects."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config

# Create database engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Create database session
Session = sessionmaker(bind=engine)
session = Session()
