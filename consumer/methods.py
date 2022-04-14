import asyncio
import datetime
import random
import time

from simple_print import sprint

from database import methods as db_methods
from producer import methods as producer_methods


async def check_host_accessibility(host: str, port: int, duration=5, delay=1):
    """
    host : str
        host ip address or hostname
    port : int
        port number
    duration : int, optional
        Total duration in seconds to wait, by default 10
    delay : int, optional
        delay in seconds between each try, by default 2
    """

    date_now = datetime.datetime.now()
    time_now = time.time()
    tmax = time.time() + duration
    while time.time() < tmax:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
            writer.close()
            await writer.wait_closed()
            response_time = time.time() - time_now
            response_time_ms = (datetime.datetime.now() - date_now).microseconds
            if response_time_ms == 0:
                response_time_ms = random.randint(1, 3)
            return True, response_time, response_time_ms
        except:
            if delay:
                await asyncio.sleep(delay)

    response_time = time.time() - time_now
    return False, response_time, 0


async def monitor(incoming_data):

    monitor_request_time = datetime.datetime.now().strftime("%H:%M")
    connection_establish, response_time, response_time_ms = await check_host_accessibility(incoming_data["monitor_host"], incoming_data["monitor_port"])

    await db_methods.insert_monitor_activity(incoming_data["monitor_id"], connection_establish, response_time, response_time_ms)
    sprint(f"Monitor {incoming_data['monitor_name']} ID={incoming_data['monitor_id']} HOST={incoming_data['monitor_host']} PORT={incoming_data['monitor_port']}", c="green", s=1, p=1)
    sprint(f"Connection establish={connection_establish} :: response_time={response_time}", c="yellow", s=1, p=1)

    if connection_establish:
        outcoming_data = {}
        outcoming_data["monitor_id"] = incoming_data["monitor_id"]
        outcoming_data["monitor_name"] = incoming_data["monitor_name"]
        outcoming_data["monitor_host"] = incoming_data["monitor_host"]
        outcoming_data["monitor_port"] = incoming_data["monitor_port"]
        outcoming_data["monitor_connection_establish"] = 1
        outcoming_data["monitor_request_time"] = monitor_request_time
        outcoming_data["monitor_response_time"] = int(response_time_ms)
        await producer_methods.internal_messager__monitor(outcoming_data)
    else:
        outcoming_data = {}
        outcoming_data["monitor_id"] = incoming_data["monitor_id"]
        outcoming_data["monitor_name"] = incoming_data["monitor_name"]
        outcoming_data["monitor_host"] = incoming_data["monitor_host"]
        outcoming_data["monitor_port"] = incoming_data["monitor_port"]
        outcoming_data["monitor_request_time"] = monitor_request_time
        outcoming_data["monitor_connection_establish"] = 0
        outcoming_data["monitor_response_time"] = 0
        await producer_methods.internal_messager__monitor(outcoming_data)

        outcoming_data = {}
        outcoming_data["monitor_id"] = incoming_data["monitor_id"]
        await producer_methods.internal_restore__restore(outcoming_data)
