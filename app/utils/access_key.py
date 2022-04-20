from aiohttp import web
import jwt
from datetime import datetime
from json import dumps

def get_jwt_dec(json):
    jwt_enc = json['jwt']
    jwt_dec = jwt.decode(jwt_enc, algorithms="HS256")
    return jwt_dec 

limit = 86400 * 2

def jwt_expired(token):
    decoded = jwt.decode(token, algorithms=["RS256"])
    if int(decoded['creation_time']) + limit <= datetime.now().timestamp():
        expired_error = dumps({"error":"jwt expired"})
        return web.Response(text=expired_error)
