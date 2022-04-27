from aiohttp import web
from jsonschema import validate
from json import dumps
import jwt

from utils.access_key import jwt_expired, get_jwt_dec
from utils.validation import validate

from db import db
from models.profile import Profile
from models.user import User

schema = {
    "type" : "object",
    "properties" : {
        "name" : {"type" : "string"},
        "jwt" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.put('/api/profiles/')
async def edit_profile(request):
    # парсим json, валидируем
    json_input = await request.json()
    error = validate(json_input, schema)
    if error: 
        web.Response(text=error)
    jwt_dec = get_jwt_dec(json_input['jwt']) 
    if not jwt_dec:
        error = dumps({"error":"wrong token"})
        return web.Response(text=error)
    # проверка досутпа jwt
    if jwt_expired(jwt_dec):
        error = dumps({"error":"expired token"})
        return web.Response(text=error)
    user_id = jwt_dec['user_id']
    # получаем имя
    name = json_input['name']
    # редактируем профиль
    await Profile.update.values(name=name).where(Profile.user_id==user_id).gino.status()
    return web.Response(text="success!")