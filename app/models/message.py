from db import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Unicode())
    image = db.Column(db.Unicode)
    publication_time = db.Column(db.Integer())
    # связи
    thread_id = db.Column(db.Integer(), db.ForeignKey('threads.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('profiles.id'))  