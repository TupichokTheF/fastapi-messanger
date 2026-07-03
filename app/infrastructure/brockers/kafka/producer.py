import json

from aiokafka.producer import AIOKafkaProducer

from app.core.settings import settings


class KafkaProducer:

    def __init__(self):
        self._producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_SERVER,
                                client_id='log_producer_1',
                                acks='all',
                                linger_ms=100,
                                value_serializer= lambda data: json.dumps(data).encode("utf-8"))

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def send_message(self, topic_name: str, message_data: dict):
        await self._producer.send(topic_name, message_data)
