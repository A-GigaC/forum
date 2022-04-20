from db import db

class Refresh_token(db.Model):
    __tablename__= 'refresh_tokens'

    id = db.Column(db.Integer(), primary_key=True)
    refresh_token = db.Column(db.Unicode())
    creation_time = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
