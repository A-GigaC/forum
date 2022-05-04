from db import db

class Profile(db.Model):
    __tablename__= 'profiles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    registration_time = db.Column(db.Integer())
    avatar = db.Column(db.Unicode())
    # связи
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

