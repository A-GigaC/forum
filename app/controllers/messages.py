from aiohttp import web
from json import dumps
from app.models.auth_key import Auth_key

from db import db
from models.message import Message
from models.profile import Profile
from models.user import User

routes = web.RouteTableDef()

@routes.post('/api/messages/')
async def create_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    # получаем профиль оп auth_key
    author_id = await Auth_key.select('user_id').where(Auth_key.auth_key==json_input['auth_key']).gino.scalar()
    author_name = await Profile.select('name').where(Profile.user_id==author_id).gino.scalar()
    # создаём новое сообщение и записываем в БД
    message = await Message.create(body=json_input['body'], 
        thread_id=int(json_input['thread']), author_id=author_id)
    # формируем ответ
    json = dumps({"id":message.id, "body":message.body, "author":{
        "name": author_name
    }})
    return web.Response(text=json)

@routes.put('/api/messages/{id}/')
async def edit_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    # получаем id сообщения
    id = int(request.match_info['id'])
    # по auth_key проверяем право на редактирование
    user_id = await User.select('id').where(User.auth_key==json_input['auth_key']).gino.scalar()
    message = await Message.get(id)
    if user_id != message.author_id:
        access_error = dumps({"error":"you are not the author"})
        return web.Response(text=access_error)
    else:
        # меняем данные
        new_body = json_input["body"]
        edited_message = await Message.update.values(body=new_body).where(Message.id==id).gino.status()
        return web.Response(text=edited_message[0])

@routes.delete('/api/messages/{id}/')
async def delete_message(request):
    # парсим json, получаем тело нового сообщения и id треда, в котором будет наше сообщние
    json_input = await request.json()
    # получаем id сообщения
    id = int(request.match_info['id'])
    # по auth_key проверяем право на редактирование
    user_id = await Auth_key.select('user_id').where(Auth_key.auth_key==json_input['auth_key']).gino.scalar()
    message = await Message.get(id)
    if user_id != message.author_id:
        access_error = dumps({"error":"you are not the author"})
        return web.Response(text=access_error)
    else:
        await Message.delete.where(Message.id==id).gino.status()
        return web.Response(text="message deleted")
    