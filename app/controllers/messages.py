from aiohttp import web
from json import dumps

from db import db
from models.message import Message
from models.profile import Profile
routes = web.RouteTableDef()

@routes.post('/api/messages/')
async def create_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
   # как выглядит message {'body': 'smth', 'thread': 'smth'}
    # создаём новое сообщение и записываем в БД
    message = await Message.create(body=json_input['body'], 
        thread_id=int(json_input['thread']), author_id=['author'])
    profile = json_input['author']
    json = dumps({"id":message.id, "body":message.body, "author":{
        "name":profile['name']
    }})
    return web.Response(text=json)

@routes.put('/api/messages/{id}/')
async def edit_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    new_body = json_input["body"]
    # получаем id сообщения
    id = int(request.match_info['id'])
    # меняем данные
    edited_message = await Message.update.values(body=new_body).where(Message.id==id).gino.status()
    return web.Response(text=edited_message[0])

@routes.delete('/api/messages/{id}/')
async def delete_message(request):
    # получаем id
    id = int(request.match_info['id'])
    await Message.delete.where(Message.id==id).gino.status()
    return web.Response(text="success!")
    