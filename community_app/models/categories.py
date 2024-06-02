from community_app import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    questions = db.relationship('Question', backref='category', lazy=True)

    def __str__(self):
        return f"Category: {self.name}"
