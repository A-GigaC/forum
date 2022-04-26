from aiohttp import web
from jsonschema import validate
from json import dumps
import jwt

from utils.access_key import jwt_expired, get_jwt_dec

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
    # парсим json, валидируем и проверяем доступ
    json_input = await request.json()
    validate(instance=json_input, schema=schema)
    jwt_dec = get_jwt_dec(json_input['jwt']) 
    # проверка доступа jwt
    jwt_expired(jwt_dec)
    user_id = jwt_dec['user_id']
    # получаем имя
    name = json_input['name']
    # редактируем профиль
    await Profile.update.values(name=name).where(Profile.user_id==user_id).gino.status()
    return web.Response(text="success!")