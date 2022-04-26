from aiohttp import web
import jwt
from datetime import datetime
from json import dumps

from utils.secret_key import secret_key

def get_jwt_dec(jwt_enc):
    jwt_dec = (jwt.decode(jwt_enc, secret_key(), 
    algorithms="HS256"))['data']
    return jwt_dec 

limit = 86400 * 2

def jwt_expired(decoded):
    if float(decoded['creation_time']) + limit <= datetime.now().timestamp():
        expired_error = dumps({"error":"jwt expired"})
        return web.Response(text=expired_error)

