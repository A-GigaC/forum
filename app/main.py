from aiohttp import web

app = web.Application()

from controllers.threads import routes as threads_routes
from controllers.messages import routes as messages_routes
from controllers.profiles import routes as profiles_routes
from controllers.auth import routes as auth_routes

app.add_routes([ *threads_routes, *messages_routes,
 *auth_routes, *profiles_routes  ])

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from db import init_db
loop.run_until_complete(init_db())

web.run_app(app, loop=loop)