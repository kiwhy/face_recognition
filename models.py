from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'usertable'

    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)