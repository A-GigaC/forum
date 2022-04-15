from hashlib import sha1

from aiohttp import web
from json import dumps

from db import db
from models.user import User
from models.profile import Profile
from models.auth_key import Auth_key

from random import choices
import string
prnt_lst = [x for x in string.printable if x not in string.whitespace]

def get_random_key():
    rnd_lst = choices(prnt_lst, k=16)
    random_key = ''.join(rnd_lst)
    return random_key

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
    auth_key = sha1(json_input['nickname']+json_input['password']+ get_random_key())
    # создаём нового юзера
    user = await User.create(nickname=json_input['nickname'],
        password=json_input['password'])
    # добавляем auth_key в БД
    await Auth_key.create(user_id=user.id, auth_key=auth_key)
    profile = await Profile.create(name=json_input['profile']['name'],
     user_id=user.id)
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
    # получаем user_id
    user_id = await User.select('id').where(
        User.password==password).gino.scalar()
    # получение аутентификационного ключа и его перезапись
    auth_key = get_random_key()
    await Auth_key.update.values(auth_key=auth_key).where(
        user_id==user_id).gino.status()
    # проверка подлинности пароля
    if password==json_input['password']:
        json = dumps({"auth_key":auth_key})
        return web.Response(text=json)
    else:
        error = json.dump({"error":"wrong password -50000 social credit"})
        return web.Response(text=error)
    
