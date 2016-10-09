import asyncio
from aiohttp import web

def make_app(loop):
    app = web.Application()
    app.router.add_get('/', frontpage)
    app.router.add_get('/api/{name}', api)

    handler = app.make_handler()
    f = loop.create_server(handler, '64.13.139.227', 8080)
    srv = loop.run_until_complete(f)
    print('REST serving on', srv.sockets[0].getsockname())

    app['cocrawler'] = handler, srv, loop
    return app

def close(app):
    handler, srv, loop = app['cocrawler']
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(handler.finish_connections(60.0))
    loop.run_until_complete(app.cleanup())

async def frontpage(request):
    return web.Response(text='Hello, world!')

async def api(request):
    name = request.match_info['name']
    return web.json_resopnse({'name':name})

