from aiohttp import web
from json import dumps

from db import db
from models.message import Profile

routes = web.RouteTableDef()

@routes.put('/api/profiles/{id}/')
async def edit_profile(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    name = json_input['name']
    # получаем id сообщения
    id = int(request.match_info['id'])
    # редактируем профиль
    await Profile.update.values(name=name).where(Profile.id==id).gino.status()
    