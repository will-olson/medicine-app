from datetime import datetime
from config import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class DrugSearchLog(db.Model):
    __tablename__ = "drug_search_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    query = db.Column(db.String(255), nullable=False)
    response_data = db.Column(db.JSON, nullable=True)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("search_logs", lazy=True))

    def __repr__(self):
        return f"<DrugSearchLog {self.query} by User {self.user_id}>"


class AdverseEvent(db.Model):
    __tablename__ = "adverse_events"

    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(255), nullable=False)
    event_description = db.Column(db.Text, nullable=False)
    demographics = db.Column(db.JSON, nullable=True)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AdverseEvent {self.drug_name}>"


class DrugRecall(db.Model):
    __tablename__ = "drug_recalls"

    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(255), nullable=False)
    recall_reason = db.Column(db.Text, nullable=False)
    recall_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<DrugRecall {self.drug_name} - {self.status}>"
