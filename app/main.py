from aiohttp import web

app = web.Application()

from controllers.threads import routes as threads_routes
from controllers.messages import routes as messages_routes
# app.add_route('/api/threads/', post_thread)
app.add_routes([ *threads_routes  ])
app.add_routes([ *messages_routes  ])

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from db import init_db
loop.run_until_complete(init_db())

web.run_app(app, loop=loop)