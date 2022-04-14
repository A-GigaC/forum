from hashlib import md5

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
    # проверка существования пользователя с введённым никнеймом
    if await User.exists(User.query.where(User.nickname == json_input['nickname'])).gino.scalar():
        nickAlreadyExists = json.dump({"error":"nickname already exists"})
        return web.Response(text=nickAlreadyExists)
    # создaём авторизационный ключ
    auth_key = md5(json_input['nickname']+json_input['password'])
    # создаём нового юзера
    user = await User.create(nickname=json_input['nickname'],
        password=json_input['password'])
    profile = await Profile.create(name=json_input['profile']['name'],
     user_id=user.id, auth_key=auth_key)
    # делаем ответ с авторизационным ключем
    json = dumps({"auth_key":auth_key})
    return web.Response(text=json)

@routes.post('/api/auth/signin/')
async def signin(request):
    # парсим json, получаем nick, psswrd
    json_input = await request.json()    
    # проверка существования пользователя с заданным никнеймом
    if not await User.exists(User.query.where(User.nickname == json_input['nickname'])).gino.scalar():
        nickDoesntExists = json.dump({"error":"nickname doesnt exists"})
        return web.Response(text=nickDoesntExists)
    # получение пароля
    password = await User.select('password').where(
        User.nickname==json_input['nickname']).gino.scalar()
    # получение аутентификационного ключа
    auth_key = await User.select('auth_key').where(
        User.nickname==json_input['nickname']).gino.scalar()
    # проверка подлинности пароля
    if password==json_input['password']:
        json = dumps({"auth_key":auth_key})
        return web.Response(text=json)
    else:
        error = json.dump({"error":"wrong password -50000 social credit"})
        return web.Response(text=error)
    
