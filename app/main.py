from aiohttp import web

app = web.Application()

from controllers.threads import routes

app.add_routes([
    *routes
])

import asyncio
from db import init_db

asyncio.get_event_loop().run_until_complete(init_db())

web.run_app(app)