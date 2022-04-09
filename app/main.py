from aiohttp import web
from math import pi

import json

app = web.Application()

routes = web.RouteTableDef()

posts = [{'name': 'fedya', 'comment': ''}]

# ТЗ
# GET /posts - возращает ВСЕ посты в json
# POST /posts - принимает в body json с постом, который нужно добавить в список постов
# Post = {
#   name: string;
#   comment: string;
# }

# https://docs.aiohttp.org/en/stable/web_reference.html#request-and-base-request
# https://docs.aiohttp.org/en/stable/web_reference.html#response-classes

@routes.get('/posts')
async def get_posts(request):
    return web.Response(text=json.dumps(posts))

@routes.post('/posts')
async def add_post(request):
    try:
        parsed_data = await request.json()
        if 'name' in parsed_data and 'comment' in parsed_data:
            if type(parsed_data['comment']) is str and type(parsed_data['name']) is str:
                post = {'name': parsed_data['name'], 'comment': parsed_data['comment']}
                posts.append(post)
                return web.Response(text='success')
            else:
                return web.Response(text='wrong fields type', status=400)
        else:
            return web.Response(text='missing keys', status=400)

    except: json.decoder.JSONDecodeError

    return web.Response(text='failed to parse json', status=400)

    
app.add_routes(routes)

web.run_app(app)