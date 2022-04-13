from aiohttp import web
from json import dumps

from db import db
from models.user import User
from models.profile import Profile

routes = web.RouteTableDef()

@routes.post('/api/auth/signup/')
async def signup(request):
    # парсим json, получаем необходимую информацию
    json_input = await request.json() 
    # создаём нового юзера
    user = await User.create(nickname=json_input['nickname'],
        password=json_input['password'])
    profile = await Profile.create(name=json_input['profile']['name'],
     user_id=user.id)
    return web.Response(text="success!")

@routes.put('/api/auth/signin/')
async def signin(request):
    # парсим json, получаем nick, psswrd
    json_input = await request.json()    
    password = await User.select('password').where(
        User.nickname==json_input['nickname'])
    if password==json_input['password']:
        json = dumps({"magic":"magic)))????!?!?!?7"})
        return web.Response(text=json)
    return web.Response(text="neudacha(-5000 social credit")
    
