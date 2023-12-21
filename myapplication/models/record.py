from sqlalchemy import func
from myapplication import db


class Record(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), unique=False, nullable=False)
    time = db.Column(db.TIMESTAMP, server_default=func.now())
    amount_of_expenditure = db.Column(db.Float(precision=2), unique=False, nullable=False)
    user = db.relationship("User", back_populates="record")
    category = db.relationship("Category", back_populates="record")

    def __init__(self, user_id, category_id, amount_of_expenditure):
        self.user_id = user_id
        self.category_id = category_id
        self.amount_of_expenditure = amount_of_expenditure
