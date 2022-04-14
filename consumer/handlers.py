from consumer import methods
from consumer import schema
from consumer.helpers import validate_request_schema


@validate_request_schema(schema.Montitor)
async def monitor(data):
    await methods.monitor(data)
