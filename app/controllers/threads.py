from aiohttp import web
from json import dumps

from db import db
from models.thread import Thread
from models.message import Message

routes = web.RouteTableDef()

@routes.post('/api/threads/')
async def create_thread(request):
    # парсим жейсон, получаем имя нового треда
    name = await request.json()
    # создаём новый тред с заданным именем и сохраняем в бд
    thread = await Thread.create(name=name['name'])
    json = dumps({ 'thread': thread.id })
    return web.Response(text=json)

@routes.get('/api/threads/{id}/')
async def get_thread_by_id(request):
    id = int(request.match_info['id'])
    # найти в базе данных нужный тред
    thread = await Thread.get(id)
    # найти все сообщения, которые связаны с этим тредом
    messages = await Message.query.where(Message.thread_id == id).gino.all()
    # собрать все данные в ответный json
    json = dumps({"thread":{"id":thread.id,
        "name": thread.name, "messages": messages }})
    return web.Response(text=json)

@routes.get('/api/threads/')
async def get_threads(request):
    #получить информацию обо всех тредах
    threads = await db.all(Thread.query)
    # собрать все данные в ответный json
    # для этого создадим массив имен и айдишников
    obj = []
    for _ in range(len(threads)):
        obj.append({"id":threads[_].id, "name":threads[_].name})
    json = dumps({"threads": obj})
    return web.Response(text=json)

