db = SessionLocal()
try:
    gestures = [
        Gesture(name="fist", output_text="Hello"),
        Gesture(name="palm", output_text="Yes"),
        Gesture(name="thumbs_up", output_text="Good")
    ]

    for g in gestures:
        if not db.query(Gesture).filter_by(name=g.name).first():
            db.add(g)

    db.commit()
    print("Database initialized")

finally:
    db.close()

