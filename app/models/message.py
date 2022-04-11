from db import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer(), primary_key=True)
    thread_id = db.Column(db.Integer(), db.ForeignKey('threads.id'))
    body = db.Column(db.Unicode())
    publication_time = db.Column(db.Date())
    