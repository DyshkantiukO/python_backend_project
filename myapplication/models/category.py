from myapplication import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    record = db.relationship("Record", back_populates="category", lazy="dynamic")

    def __init__(self, name):
        self.name = name
