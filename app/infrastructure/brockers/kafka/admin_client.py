import asyncio

from contextlib import asynccontextmanager

from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError


@asynccontextmanager
async def kafka_admin():
    admin = AIOKafkaAdminClient(bootstrap_servers="localhost:9092")
    await admin.start()
    try:
        yield admin
    finally:
        await admin.close()

async def create_topic(admin: AIOKafkaAdminClient):
    app_logs_topic = NewTopic(
        name="app_logs",
        num_partitions=10,
        replication_factor=1,
        topic_configs={
            "retention.ms": str(1000 * 3600 * 24)
        }
    )
    try:
        await admin.create_topics([app_logs_topic])
    except TopicAlreadyExistsError:
        pass

async def describe_topics_information(topics: list[str], admin: AIOKafkaAdminClient):
    info = await admin.describe_topics(list(topics))
    return info


async def main():
    async with kafka_admin() as admin:
        await create_topic(admin)
        await describe_topics_information(['app_logs'], admin)

if __name__ == "__main__":
    asyncio.run(main())


