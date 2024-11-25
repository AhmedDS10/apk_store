from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class APKFile(Base):
    __tablename__ = 'apk_files'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    description = Column(String(500))
    icon = Column(LargeBinary)  # Store icon as binary data
    file = Column(LargeBinary)  # Store APK file as binary data
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    uploaded_by = Column(Integer)  # User ID who uploaded the file

# Create database engine
engine = create_engine('sqlite:///apk_store.db')
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(bind=engine)