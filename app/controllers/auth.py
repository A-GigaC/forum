from hashlib import sha256

from aiohttp import web
from jsonschema import validate
from json import dumps
from datetime import datetime
from utils.access_key import jwt_expired

from db import db
from models.user import User
from models.profile import Profile
from models.auth import Auth_key

signup_sch = {
    "type" : "object",
    "properties" : {
        "nickname" : {"type" : "string"},
        "password" : {"type" : "string"},
        "name" : {"type" : "string"},
    },
}
signin_sch = {
    "type" : "object",
    "properties" : {
        "nickname" : {"type" : "string"},
        "password" : {"type" : "string"},
    },
}
get_jwt_sch = {
    "type" : "object",
    "properties" : {
        "user_id" : {"type" : "number"},
        "auth_key" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.post('/api/auth/signup/')
async def signup(request):
    # парсим json, получаем необходимую информацию и валидируем
    json_input = await request.json() 
    validate(instance=json_input, schema=signup_sch)
    # проверка существования пользователя с введённым никнеймом
    if await User.exists(User.query.where(User.nickname == json_input['nickname'])).gino.scalar():
        nickAlreadyExists = json.dump({"error":"nickname already exists"})
        return web.Response(text=nickAlreadyExists)
    # создaём авторизационный ключ
    auth_key = sha256(json_input['nickname']+json_input['password'])
    # создаём нового юзера
    user = await User.create(nickname=json_input['nickname'],
        password=json_input['password'])
    profile = await Profile.create(name=json_input['profile']['name'],
     user_id=user.id)
    # добавляем ключ
    await Auth_key.create(auth_key=auth_key, user_id=user.id, status="false")
    # делаем ответ с авторизационным ключем
    json = dumps({"auth_key":auth_key})
    return web.Response(text=json)

@routes.post('/api/auth/signin/')
async def signin(request):
    # парсим json, получаем необходимую информацию и валидируем
    json_input = await request.json() 
    validate(instance=json_input, schema=signin_sch)  
    # проверка существования пользователя с заданным никнеймом
    if not await User.exists(User.query.where(User.nickname == json_input['nickname'])).gino.scalar():
        nickDoesntExists = dumps({"error":"nickname doesnt exists"})
        return web.Response(text=nickDoesntExists)
    # получение пароля
    password = await User.select('password').where(
        User.nickname==json_input['nickname']).gino.scalar()
    # проверка подлинности пароля
    if password==json_input['password']:
        await Auth_key.update(status="true").apply()
        jwt = dumps({"user_id": await User.id.where(password=password).gino.scalar(), 
        "datetime":datetime.now().date()})
        jwt_enc = jwt.encode(jwt, algorithm="HS256")
        return web.Response(text=jwt_enc)
    else:
        error = dumps({"error":"wrong password -50000 social credit"})
        return web.Response(text=error)
    
@routes.post('/api/auth/get_jwt/')
async def get_jwt(request):
    # парсим json, получаем необходимую информацию и валидируем
    json_input = await request.json() 
    validate(instance=json_input, schema=get_jwt_sch) 
    user_id = json_input['user_id']
    input_auth_key = json_input['auth_key']
    auth_key = await Auth_key.select('auth_key').where(user_id=user_id).gino.scalar()
    status = await Auth_key.select('status').where(user_id=user_id).gino.scalar()
    if auth_key != input_auth_key:
        wrong_key = dumps({"error":"auth_key is wrong"})
        return web.Response(text=wrong_key)
    if status == "true":
        jwt = dumps({"user_id": user_id,
        "datetime":datetime.now().date()})
        jwt_enc = jwt.encode(jwt, algorithm="HS256")
        json = dumps({"jwt":jwt_enc})
        return web.Response(text=json)
    else:
        json = dumps({"error":"account logouted"})
        return web.Response(text=json)
    
@routes.post('/api/auth/logout/')
async def logout(request):
    pass