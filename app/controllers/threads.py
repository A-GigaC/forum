from aiohttp import web
from models.thread import create_thread

routes = web.RouteTableDef()

@routes.post('/api/threads/')
async def post_thread(request):
    name = request.text()
    # create_thread(name)
    print(name)
    
    return web.Response()

