from sqlalchemy import func
from myapplication import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    user_money = db.relationship("Account", uselist=False, back_populates="user_account")
    record = db.relationship("Record", back_populates="user", lazy="dynamic")

    def __init__(self, name):
        self.name = name


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    money = db.Column(db.Float(precision=2), unique=False, nullable=False)
    user_account = db.relationship("User", back_populates="user_money")

    def __init__(self, user_id, money):
        self.user_id = user_id
        self.money = money


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    record = db.relationship("Record", back_populates="category", lazy="dynamic")

    def __init__(self, name):
        self.name = name


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
