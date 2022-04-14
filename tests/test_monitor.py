import pprint

import pytest

from consumer import methods


@pytest.mark.asyncio
async def test_monitor():
    """
    {
        "message":"test message",
        "monitor_port":"443",
        "source":"test",
        "username":"test"
    }

    """
    json_rq = {"monitor_id": "2", "monitor_name": "Makar Monitor", "monitor_host": "iqsssos.ru", "monitor_port": "443"}
    pprint.pprint(json_rq)
    result = await methods.monitor(json_rq)
    assert result
