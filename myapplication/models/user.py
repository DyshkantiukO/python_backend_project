from myapplication import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    user_money = db.relationship("Account", uselist=False, back_populates="user_account")
    record = db.relationship("Record", back_populates="user", lazy="dynamic")

    def __init__(self, name, password):
        self.name = name
        self.password = password
