from aiohttp import web
from jsonschema import validate
from json import dumps
import jwt

from db import db
from models.profile import Profile

schema = {
    "type" : "object",
    "properties" : {
        "name" : {"type" : "string"},
        "auth_key" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.put('/api/profiles/{id}/')
async def edit_profile(request):
    # парсим json, валидируем и проверяем доступ
    json_input = await request.json()
    validate(instance=json_input, schema=schema)
    
    # получаем имя
    name = json_input['name']
    # редактируем профиль
    await Profile.update.values(name=name).where(Profile.id==id).gino.status()
    return web.Response(text="success!")