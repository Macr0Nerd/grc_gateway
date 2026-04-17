"""Webserver abstracts."""

import logging
from typing import Callable

from grc.plugins.logging.abstract import TemplateStringAdapter

logger = TemplateStringAdapter(logging.getLogger(__name__))


class App:
    """GRC Gateway ASGI application."""

    async def __call__(
        self, scope: dict, receive: Callable, send: Callable
    ) -> None:
        """Application factory function.

        Args:
            scope (dict): Application scope
            receive (Callable): Application receive channel
            send (Callable): Application send channel

        Raises:
            RuntimeError: Application doesn't support WebSocket.
        """
        if scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    logger.info('Application is starting up...')
                    await send({'type': 'lifespan.startup.complete'})
                elif message['type'] == 'lifespan.shutdown':
                    logger.info('Application is shutting down...')
                    await send({'type': 'lifespan.shutdown.complete'})
                    return

        elif scope['type'] == 'http':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [(b'content-type', b'text/plain')],
            })
            await send({'type': 'http.response.body', 'body': b'Hello, World!'})
        else:
            raise RuntimeError("This server doesn't support WebSocket.")
