from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///gestures.db", echo=True)  # SQLite DB file in backend folder
SessionLocal = sessionmaker(bind=engine)

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

# Creates all tables if they don't exist
Base.metadata.create_all(bind=engine)
