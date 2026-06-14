from app.core.log_config import AbstractHandler

from asyncio import Queue, AbstractEventLoop


class KafkaHandler(AbstractHandler):

    def __init__(self, queue: Queue, loop: AbstractEventLoop):
        super().__init__()
        self._queue = queue
        self._loop = loop

    def emit(self, record):
        payload = {
            'message': record.getMessage(),
            'level': record.levelname,
            'created_at': record.created
        }
        self._loop.call_soon_threadsafe(self._add_message_to_queue, payload)

    def _add_message_to_queue(self, payload: dict):
        self._queue.put_nowait(payload)