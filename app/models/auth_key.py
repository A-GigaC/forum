from db import db

class Auth_key(db.Model):
    __tablename__ = 'auth_keys'

    id = db.Column(db.Integer(),
     primary_key=True)
    # пока не jwt
    auth_key = db.Column(db.Unicode())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))