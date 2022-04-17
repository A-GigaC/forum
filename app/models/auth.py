from db import db

class Auth_key(db.Model):
    __tablename__= 'auth_keys'

    id = db.Column(db.Integer(), primary_key=True)
    auth_key = db.Column(db.Unicode())
    auth_data = db.Column(db.Date())
    status = db.Column(db.Unicode())
    # связи
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
