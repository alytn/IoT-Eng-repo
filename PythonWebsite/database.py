from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    email = db.Column("email", db.String(100))
    score = db.Column("score", db.Integer)

    def __init__(self, username, email="", score=0):
        self.username = username
        self.email = email
        self.score = score