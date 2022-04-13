from aiohttp import web
from json import dumps

from db import db
from models.message import Message

routes = web.RouteTableDef()

@routes.post('/api/messages/')
async def create_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
   # как выглядит message {'body': 'smth', 'thread_id': 'smth'}
    # создаём новое сообщение и записываем в БД
    message = await Message.create(body=json_input['body'], 
        thread_id=int(json_input['thread_id']))
    # формируем ответный json
    json = dumps({"thread":message.thread_id})
    return web.Response(text=json)

@routes.put('/api/messages/{id}/')
async def edit_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    new_body = json_input["body"]
    # получаем id сообщения
    id = int(request.match_info['id'])
    # меняем данные
    await Message.update.values(body=new_body).where(Message.id==id).gino.status()
    return web.Response(text="success!")

@routes.delete('/api/messages/{id}/')
async def delete_message(request):
    # получаем id
    id = int(request.match_info['id'])
    await Message.delete.where(Message.id==id).gino.status()
    return web.Response(text="success!")
    