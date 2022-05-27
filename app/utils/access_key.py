import jwt
from datetime import datetime

from utils.secret_key import secret_key

def get_jwt_dec(jwt_enc):
    try:
        jwt_dec = (jwt.decode(jwt_enc, secret_key(), 
        algorithms="HS256"))['data']
        return jwt_dec 
    except Exception:
        return False

limit = 86400 * 2

def jwt_expired(decoded):
    if float(decoded['creation_time']) + limit <= datetime.now().timestamp():
        return True
    else:
        return False