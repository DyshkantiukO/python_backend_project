from myapplication import db


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    money = db.Column(db.Float(precision=2), unique=False, nullable=False)
    user_account = db.relationship("User", back_populates="user_money")

    def __init__(self, user_id, money):
        self.user_id = user_id
        self.money = money
