from hashlib import sha256
import datetime

from aiohttp import web
import jwt
from jsonschema import validate
from json import dumps
from datetime import datetime

from db import db
from models.user import User
from models.profile import Profile
from models.rt import Refresh_token

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))

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
        "nickname" : {"type" : "string"},        
        "refresh_token" : {"type" : "string"},
    },
}
logout_sch = {
    "type" : "object",
    "properties" : {
        "refresh_token" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.post('/api/auth/signup/')
async def signup(request):
    # парсим json, получаем необходимую информацию и валидируем
    json_input = await request.json() 
    validate(instance=json_input, schema=signup_sch)
    # проверка существования пользователя с введённым никнеймом
    if await db.scalar(db.exists(User.query.where(User.nickname == json_input['nickname'])).select()):
        nickAlreadyExists = dumps({"error":"nickname already exists"})
        return web.Response(text=nickAlreadyExists)
    else:
        # создаём нового юзера
        user = await User.create(nickname=json_input['nickname'],
            password=json_input['password'])
        profile = await Profile.create(name=json_input['profile']['name'],
        user_id=user.id)
        json = dumps({"success":"you can login"})
        return web.Response(text=json)

@routes.post('/api/auth/signin/')
async def signin(request):
    # парсим json, получаем необходимую информацию и валидируем
    json_input = await request.json() 
    validate(instance=json_input, schema=signin_sch)  
    # проверка существования пользователя с заданным никнеймом
   # await db.scalar(db.exists(User.query.where(User.email == email)).select())
    if not await db.scalar(db.exists(User.query.where(User.nickname == json_input['nickname'])).select()):
        nickDoesntExists = dumps({"error":"nickname doesnt exists"})
        return web.Response(text=nickDoesntExists)
    # получение пароля
    password = await User.select('password').where(
        User.nickname==json_input['nickname']).gino.scalar()
    # проверка подлинности пароля
    if password==json_input['password']:
        user = await User.query.where(User.password==password).gino.first()
        user_id = user.id
        # создаём refresh_token
        refresh_token = str(sha256(bytes(json_input['nickname']+str(datetime.now().timestamp()),
            encoding="utf8")).hexdigest())
        await Refresh_token.create(refresh_token=refresh_token,
            user_id=user_id, creation_time=datetime.now().timestamp())
        # создаём jwt
        jwt_ = [{"user_id": user_id, 
        "creation_time":datetime.now().timestamp()}]
        jwt_enc = jwt.encode({"data":jwt_}, SECRET_KEY, algorithm="HS256")
        # формируем ответ
        json = dumps({"jwt":str(jwt_enc), "refresh_token":str(refresh_token)})
        return web.Response(text=json)
    else:
        error = dumps({"error":"wrong password -50000 social credit"})
        return web.Response(text=error)
    
@routes.post('/api/auth/get_jwt/')
async def get_jwt(request):
    # парсим и валидируем json
    json_input = await request.json() 
    validate(instance=json_input, schema=get_jwt_sch)
    input_refresh_token = json_input['refresh_token']
    nickname = json_input['nickname']
    # проверяем существования введённого refresh_token
    if not await db.scalar(db.exists().where(Refresh_token.refresh_token == input_refresh_token).select()):
        error = dumps({"error":"wrong RT"})
        return web.Response(text=error)
    old_refresh_token = await Refresh_token.select('creation_time').where(
        Refresh_token.refresh_token==input_refresh_token).gino.scalar()
    user_id = await User.select('id').where(User.nickname==nickname).gino.scalar()
    #проверка срока годности ключа
    if old_refresh_token + 86400 * 15 < datetime.now().timestamp():
        expired_rt = dumps({"error":"expired RT -5000 social credit"})
        return web.Response(text=expired_rt)
    else:
        # всё верно!     
        # создаём новый refresh токен
        refresh_token = str(sha256(bytes(json_input['nickname']+str(datetime.now().timestamp()),
            encoding="utf8")).hexdigest())
        Refresh_token.update.values(refresh_token=refresh_token, 
        creation_time=datetime.now().timestamp())
        # создаём jwt
        jwt_ = [{"user_id": user_id, 
        "creation_time":datetime.now().timestamp()}]
        jwt_enc = jwt.encode({"data":jwt_}, SECRET_KEY, algorithm="HS256")
        # формируем ответ
        json = dumps({"jwt":str(jwt_enc), "refresh_token":str(refresh_token)})
        return web.Response(text=json)

@routes.post('/api/auth/logout/')
async def logout(request):
    # парсим json, получаем необходимую информацию и валидируем
    json_input = await request.json() 
    validate(instance=json_input, schema=logout_sch)
    input_refresh_token = json_input['refresh_token']
    # проверяем существования введённого refresh_token
    refresh_token = await Refresh_token.query.where(Refresh_token.refresh_token==input_refresh_token).gino.first()
    if refresh_token is None:
        error = dumps({"error":"wrong RT"})
        return web.Response(text=error)
    # удаляем старый RT
    await refresh_token.delete()
    # формируем ответ
    json = dumps({"status":"200 OK"})
    return web.Response(text=json)