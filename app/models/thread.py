from db import db

class Thread(db.Model):
    __tablename__ = 'threads'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    author = db.Column(db.Integer(), db.ForeignKey('profiles.id'))