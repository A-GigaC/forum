from aiohttp import web
from datetime import datetime

from json import dumps
from jsonschema import validate
from utils.access_key import jwt_expired, get_jwt_dec
from utils.message_ import message_access

from db import db
from models.message import Message
from models.profile import Profile
from models.user import User

import os.path
import pathlib

create_sch = {
    "type" : "object",
    "properties" : {
        "body" : {"type" : "string"},
        "thread" : {"type" : "number"},    
    },
}
edit_sch = {
    "type" : "object",
    "properties" : {
        "body" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.post('/api/messages/')
async def create_message(request):
    # парсим json, валидируем и проверяем доступ
    json_input = await request.json()
    error = validate(json_input, create_sch)
    if error: 
        web.Response(text=error)
    jwt = request.headers['Authorization']
    jwt_dec = get_jwt_dec(jwt)
    if not jwt_dec:
        error = dumps({"error":"wrong token"})
        return web.Response(text=error)        
    # проверка досутпа jwt
    if jwt_expired(jwt_dec):
        error = dumps({"error":"expired token"})
        return web.Response(text=error)
    # получаем профиль <- user_id <- jwt_dec
    author_id = await Profile.select('id').where(Profile.user_id==jwt_dec['user_id']).gino.scalar()
    author_name = await Profile.select('name').where(Profile.user_id==author_id).gino.scalar()
    # создаём новое сообщение и записываем в БД
    message = await Message.create(
        body=json_input['body'], thread_id=int(json_input['thread']),
        publication_time=datetime.now().timestamp(), author_id=author_id 
    )
    # формируем ответ
    json = dumps({
        "id":message.id, 
        "body":message.body, 
        "author":{
            "publication_time": message.publication_time,
            "name": author_name,}
            })
    return web.Response(text=json)

@routes.post('/api/messages/{id}/images/')
async def add_image(request):
    # получаем имя
    jwt = request.headers['Authorization']
    jwt_dec = get_jwt_dec(jwt) 
    if not jwt_dec:
        error = dumps({"error":"wrong token"})
        return web.Response(text=error)
    # проверка досутпа jwt
    if jwt_expired(jwt_dec):
        error = dumps({"error":"expired token"})
        return web.Response(text=error)
    # id изображения
    id = request.rel_url.query['id']
    # получаем изображение
    image = await request.read()
    # создаём и открываем файл
    save_path = pathlib.Path(__file__).parent.resolve() + '/files/'
    file_name = f'{id}_message'
    completeName = os.path.join(save_path, file_name)
    with open(completeName, "wb") as new_image:
        new_image.write(image)
    new_image.close()
    # response
    return web.Response(text="200OK")

@routes.put('/api/messages/{id}/')
async def edit_message(request):
    # парсим json, валидируем и проверяем доступ
    json_input = await request.json()
    error = validate(json_input, edit_sch)
    if error: 
        web.Response(text=error)
    jwt = request.headers['Authorization']
    jwt_dec = get_jwt_dec(jwt)
    if not jwt_dec:
        error = dumps({"error":"wrong token"})
        return web.Response(text=error)
    # проверка досутпа jwt
    if jwt_expired(jwt_dec):
        error = dumps({"error":"expired token"})
        return web.Response(text=error)
    # получаем id сообщения
    id = int(request.match_info['id'])
    # по jwt проверяем право на редактирование
    error = await message_access(jwt_dec)
    if error:
        return web.Response(text=error)
    # меняем данные
    new_body = json_input["body"]
    edited_message = await Message.update.values(body=new_body).where(Message.id==id).gino.status()
    return web.Response(text=edited_message[0])

@routes.delete('/api/messages/{id}/')
async def delete_message(request):
    # валидируем jwt
    jwt = request.headers['Authorization']
    jwt_dec = get_jwt_dec(jwt)
    if not jwt_dec:
        error = dumps({"error":"wrong token"})
        return web.Response(text=error)
    # проверка досутпа jwt
    if jwt_expired(jwt_dec):
        error = dumps({"error":"expired token"})
        return web.Response(text=error)
    # получаем id сообщения
    id = int(request.match_info['id'])
    # по auth_key проверяем право на редактирование
    error = await message_access(jwt_dec)
    if error:
        return web.Response(text=error)
    await Message.delete.where(Message.id==id).gino.status()
    return web.Response(text="message deleted")
    
@routes.get('/api/profiles/{id}/message/')
async def get_avatar(request):
    # получаем name 
    id = int(request.match_info['id'])
    # получение Message -> path_to_image -> image
    message = await Message.where(Message.id == id).gino.scalar()
    path_to_image = message.image
    file_name = f'{id}_image'
    completeName = os.path.join(path_to_image, file_name)
    with open(completeName, "wb") as image:
        pass
    # возвращаем аватар
    content = image
    return web.Response(body=content)