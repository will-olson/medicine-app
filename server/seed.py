from config import create_app, db
from models import User, DrugSearchLog, AdverseEvent, DrugRecall
from datetime import datetime
from werkzeug.security import generate_password_hash  # For hashing passwords

# Create an app instance
app = create_app()

# Seed data for testing
def seed_database():
    with app.app_context():
        # Delete all existing data (optional, to start fresh)
        db.drop_all()
        db.create_all()

        # Create sample users (hashing passwords)
        user1 = User(username="john_doe", email="john@example.com", password=generate_password_hash("hashedpassword1"))
        user2 = User(username="jane_smith", email="jane@example.com", password=generate_password_hash("hashedpassword2"))
        
        # Add users to session
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        
        search_log1 = DrugSearchLog(
            user_id=user1.id, query="Aspirin", response_data={"drug_name": "Aspirin", "details": "Some details about Aspirin"})
        search_log2 = DrugSearchLog(
            user_id=user2.id, query="Ibuprofen", response_data={"drug_name": "Ibuprofen", "details": "Some details about Ibuprofen"})

        db.session.add(search_log1)
        db.session.add(search_log2)
        db.session.commit()

        
        event1 = AdverseEvent(drug_name="Aspirin", event_description="Headache", demographics={"age": 45, "sex": "M"})
        event2 = AdverseEvent(drug_name="Ibuprofen", event_description="Nausea", demographics={"age": 30, "sex": "F"})

        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()

        
        recall1 = DrugRecall(drug_name="Aspirin", recall_reason="Packaging defect", recall_date=datetime.utcnow(), status="Recalled")
        recall2 = DrugRecall(drug_name="Ibuprofen", recall_reason="Contamination", recall_date=datetime.utcnow(), status="Recalled")

        db.session.add(recall1)
        db.session.add(recall2)
        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
