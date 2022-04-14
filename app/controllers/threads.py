from aiohttp import web
from json import dumps

from db import db
from models.thread import Thread
from models.message import Message
from models.profile import Profile
from models.user import User

routes = web.RouteTableDef()

@routes.post('/api/threads/')
async def create_thread(request):
    # парсим json, получаем имя нового треда и auth_key
    json_input = await request.json()
    # получаем автора по auth_key
    author_id = await User.select('id').where(User.auth_key==json_input['auth_key']).gino.scalar()
    author_name = await Profile.select('name').where(Profile.user_id==author_id).gino.scalar()
    # создаём новый тред с заданным именем и сохраняем в бд
    thread = await Thread.create(name=json_input['name'], author=author_name)
    json = dumps({ 'thread': thread.id })
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
                "author": {
                    "name": last_message_author.name,
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

