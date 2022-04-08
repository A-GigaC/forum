from aiohttp import web

from app.controllers.math import routes as math_routes

app = web.Application()

app.add_routes(math_routes)

web.run_app(app)