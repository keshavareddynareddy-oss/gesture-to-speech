from database import SessionLocal, Gesture

db = SessionLocal()

letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

for letter in letters:
    exists = db.query(Gesture).filter_by(name=letter).first()
    if not exists:
        gesture = Gesture(name=letter, output_text=letter)
        db.add(gesture)

db.commit()
db.close()

print("Gestures added successfully!")
