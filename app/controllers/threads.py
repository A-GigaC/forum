from venv import create
from aiohttp import web

from jsonschema import validate
from json import dumps
from utils.access_key import jwt_expired
import jwt

from db import db
from models.thread import Thread
from models.message import Message
from models.profile import Profile
from models.user import User

create_sch = {
    "type" : "object",
    "properties" : {
        "jwt" : {"type" : "string"},
        "name" : {"type" : "string"},
    },
}
routes = web.RouteTableDef()

@routes.post('/api/threads/')
async def create_thread(request):
    # парсим json, валидируем получаем имя нового треда 
    json_input = await request.json()
    validate(instance=json_input, schema=create_sch)
    jwt_enc = json_input['jwt']
    jwt_dec = jwt.decode(jwt_enc, algorithms="HS256")
    jwt_expired(jwt_dec)
    # получаем автора по user_id
    author_name = await Profile.select('name').where(Profile.user_id==jwt_dec['user_id']).gino.scalar()
    # создаём новый тред с заданным именем и сохраняем в бд
    thread = await Thread.create(name=json_input['name'], author=author_name)
    json = dumps({'thread': thread.id })
    return web.Response(text=json)

@routes.get('/api/threads/{id}/')
async def get_thread_by_id(request):
    id = int(request.match_info['id'])
    # найти в базе данных нужный тред
    thread = await Thread.get(id)
    # найти все сообщения, которые связаны с этим тредом
    messages = await Message.query.where(Message.thread_id == id).gino.all()
    print(messages)
    last_message = messages[-1]
    print(last_message)
    last_message_author = await Profile.get(last_message.author_id)
    print(last_message_author)

    # собрать все данные в ответный json
    json = dumps({
        "thread": {
            "id": thread.id,
            "name": thread.name,
            "last_message": {
                "id": last_message.id,
                "body": last_message.body,
                "publication_time" : last_message.publication_time,
                "author": {
                    "name": last_message_author.name,
                    "registration_time" : last_message_author.registration_time,
                }
            }
        }
    })
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

