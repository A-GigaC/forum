from db import db

class Profile(db.Model):
    __tablename__= 'profiles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    registration_time = db.Column(db.Date())
    # связи
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    message_id = db.Column(db.Integer(), db.ForeignKey('messages.id'))