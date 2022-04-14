from pydantic import BaseModel
from pydantic import Field


class PingHost(BaseModel):
    host: str = Field(description="Host")


class Montitor(BaseModel):
    monitor_id: int = Field()
    monitor_name: str = Field()
    monitor_host: str = Field()
    monitor_port: int = Field()
