from aiohttp import web
from math import pi


routes = web.RouteTableDef()

# DONE
@routes.get('/square')
async def get_square(request):
    print(request.query)
    return web.Response(text=f"your square is {float(request.query['number']) ** 2}")

# DONE
@routes.get('/pi')
async def get_pi(request):
    return web.Response(text=f"{pi}")
