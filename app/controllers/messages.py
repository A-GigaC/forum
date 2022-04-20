from aiohttp import web
import datetime

from json import dumps
from jsonschema import validate
from utils.access_key import jwt_expired, get_jwt_dec
from utils.message_ import message_access

from db import db
from models.message import Message
from models.profile import Profile
from models.user import User

create_sch = {
    "type" : "object",
    "properties" : {
        "jwt" : {"type" : "string"},
        "body" : {"type" : "string"},
        "thread" : {"type" : "number"},    
    },
}
edit_sch = {
    "type" : "object",
    "properties" : {
        "jwt" : {"type" : "string"},
        "body" : {"type" : "string"},
    },
}
delete_sch = {
    "type" : "object",
    "properties" : {
        "jwt" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.post('/api/messages/')
async def create_message(request):
    # парсим и валидируем json, проверяем jwt
    json_input = await request.json()
    validate(instance=json_input, schema=create_sch)
    jwt_dec = get_jwt_dec(json_input)  
    jwt_expired(jwt_dec)    
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

@routes.put('/api/messages/{id}/')
async def edit_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    validate(instance=json_input, schema=edit_sch)
    jwt_dec = get_jwt_dec(json_input)  
    jwt_expired(jwt_dec)
    # получаем id сообщения
    id = int(request.match_info['id'])
    # по jwt проверяем право на редактирование
    await message_access(jwt_dec)
    # меняем данные
    new_body = json_input["body"]
    edited_message = await Message.update.values(body=new_body).where(Message.id==id).gino.status()
    return web.Response(text=edited_message[0])

@routes.delete('/api/messages/{id}/')
async def delete_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    validate(instance=json_input, schema=delete_sch)
    jwt_dec = get_jwt_dec(json_input)  
    jwt_expired(jwt_dec)
    # получаем id сообщения
    id = int(request.match_info['id'])
    # по auth_key проверяем право на редактирование
    await message_access(jwt_dec)
    
    await Message.delete.where(Message.id==id).gino.status()
    return web.Response(text="message deleted")
    