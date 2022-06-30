from aiohttp.web import Request


class AuthorizedRequest(Request):

    def __init__(self, jwt_dec, *arg, **kw):
        self.jwt_dec = jwt_dec  
        super().__init__(*arg, **kw)


# ###
# jwt = request.headers['Authorization']
# jwt_dec = get_jwt_dec(jwt)
# if not jwt_dec:
#     # error = dumps({"error":"wrong token"})
#     return web.Response(text="403")
# ###
from aiohttp.web import Response

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



LIMIT = 172800

def jwt_expired(decoded):
    if float(decoded['creation_time']) + LIMIT <= datetime.now().timestamp():
        return True
    else:
        return False

###
def JWTGuard():
    def decorator(controller):
        async def wrapped(request):
            jwt_enc = request.headers['Authorization']
            jwt_dec = get_jwt_dec(jwt_enc)
            if not jwt_dec:
                return Response(text="403")
            else:
                expired = jwt_expired(jwt_dec)
                if expired:
                    return Response(text="401")
                else:
                    authorized_request = AuthorizedRequest(jwt_dec, request)
                    return controller(authorized_request)
        return wrapped
    return decorator