from aiohttp import web
from json import dumps

from models.profile import Profile
from models.message import Message
from db import db

async def message_access(jwt_dec):
    id_from_jwt = jwt_dec['user_id']
    author_id = await Profile.select("id").where(user_id=id_from_jwt).gino.scalar()
    message = await Message.get(id)    
    if author_id != message.author_id:
        access_error = dumps({"error":"you are not the author"})
        return web.Response(text=access_error)