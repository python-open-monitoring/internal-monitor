import datetime
import json
from contextlib import asynccontextmanager

import aiormq
from simple_print import sprint

from settings import AMQP_URI


@asynccontextmanager
async def rabbitmq_get_channel():
    connection = await aiormq.connect(AMQP_URI)
    try:
        channel = await connection.channel()
        yield channel
    finally:
        await connection.close()


async def internal_messager__monitor(outcoming_data):
    time_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    sprint(f"AMQP PRODUCER:     internal_messager__monitor time={time_now} {outcoming_data}", с="cyan", s=1, p=1)

    outcoming_data_bytes = json.dumps(outcoming_data).encode()
    async with rabbitmq_get_channel() as channel:
        await channel.basic_publish(outcoming_data_bytes, routing_key=f"monitoring:internal__messager:monitor")


async def internal_restore__restore(outcoming_data):
    time_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    sprint(f"AMQP PRODUCER:     internal_restore__restore time={time_now} {outcoming_data}", с="cyan", s=1, p=1)

    outcoming_data_bytes = json.dumps(outcoming_data).encode()
    async with rabbitmq_get_channel() as channel:
        await channel.basic_publish(outcoming_data_bytes, routing_key=f"monitoring:internal_restore:restore")
