from aiohttp import web



app = web.Application()

routes = web.RouteTableDef()



app.add_routes(routes)

web.run_app(app)