import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

# 🔒 ABSOLUTE path to backend/gestures.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gestures.db")

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Gesture(Base):
    __tablename__ = "gestures"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    output_text = Column(String)

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    gesture = Column(String)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables in the CORRECT database
Base.metadata.create_all(bind=engine)
