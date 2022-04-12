from aiohttp import web
from json import dumps

from jsonschema import validate

from models.thread import Thread
from models.message import Message

schema = {
    "type" : "object",
    "properties" : {
        "name" : { "type" : "string" },
    },
}

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