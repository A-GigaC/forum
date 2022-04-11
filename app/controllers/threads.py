from aiohttp import web
from models.thread import create_thread
import json
from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "name" : {"type" : "string"},
    },
}

routes = web.RouteTableDef()

@routes.post('/api/threads/')
async def post_thread(request):
    name = await request.json()
    print(name)
    validate(instance=name, schema=schema)
    await create_thread(name)
    return web.Response()

