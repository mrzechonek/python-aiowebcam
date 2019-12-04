import asyncio
import contextlib
import logging
import os
import pkg_resources

import aiohttp_jinja2

from aiohttp import web
from jinja2 import PackageLoader


def run_app(host, port, *, routes, tasks=None):
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-10s %(levelname)-8s %(filename)12s:%(lineno)3s  %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %T')

    tasks = tasks or []

    app = web.Application()
    aiohttp_jinja2.setup(app, loader=PackageLoader('aiowebcam', 'templates'))

    app.add_routes(routes)
    app.add_routes([
        web.static('/static', pkg_resources.resource_filename('aiowebcam', 'static'))
    ])

    app['static_root_url'] = '/static'

    loop = asyncio.get_event_loop()

    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())

    site = web.TCPSite(runner, host, port)
    loop.run_until_complete(site.start())

    if tasks:
        loop.run_until_complete(asyncio.gather(*tasks))
    else:
        loop.run_forever()
