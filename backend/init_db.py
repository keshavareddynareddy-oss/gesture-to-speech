from database import engine, SessionLocal
from models import Base, Gesture

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Insert sample gestures
gestures = [
    Gesture(name="fist", output_text="Hello"),
    Gesture(name="palm", output_text="Yes"),
    Gesture(name="thumbs_up", output_text="Good")
]

for g in gestures:
    if not db.query(Gesture).filter_by(name=g.name).first():
        db.add(g)

db.commit()
db.close()

print("Database initialized")
