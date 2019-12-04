#!env python3

import asyncio
import logging
import traceback
from contextlib import suppress

from aiohttp import web
import aiohttp_jinja2

from aiowebcam.server import run_app


class AioWebcam:
    def __init__(self):
        self.logger = logging.getLogger('stream')
        self.header = b''
        self.queues = set()
        self.stream_token = 'supersecret'

    async def video_out(self, request):
        socket = web.WebSocketResponse(compress=False)
        await socket.prepare(request)

        try:
            self.logger.info('Stream open')
            await socket.send_bytes(self.header)

            queue = asyncio.Queue(maxsize=1)
            self.queues.add(queue)

            while not socket.closed:
                chunk = await queue.get()
                await socket.send_bytes(chunk)
        except Exception as ex:
            traceback.print_exc()
        finally:
            self.logger.info('Stream closed')
            self.queues.remove(queue)

        return socket

    async def video_header(self, request):
        if request.query['s'] == self.stream_token:
            self.header = await request.content.read()

        return web.Response(text='',
                            content_type='application/json')

    async def video_chunks(self, request):
        if request.query['s'] == self.stream_token:
            chunk = await request.content.read()

            for queue in self.queues:
                with suppress(asyncio.QueueFull):
                    queue.put_nowait(chunk)

        return web.Response(text='',
                            content_type='application/json')

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}


def aiowebcam(argv=None):
    app = AioWebcam()

    run_app(
        host='localhost',
        port=8080,
        routes=[
            web.get('/', app.index),
            web.get('/api/v1/video/out', app.video_out),
            web.put('/api/v1/video/header', app.video_header),
            web.put('/api/v1/video/chunks', app.video_chunks),
        ],
    )
