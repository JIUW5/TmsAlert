from pydantic import BaseModel, Field


class Labels(BaseModel):
    name: str = Field(..., description='service name label')
    hostname: str = Field(..., description='host name label')
    ex: str | None = Field(default=None, description='exchange/trading condition label')


class N9eEvent(BaseModel):
    labels: Labels = Field(alias='labels')
    status: str = Field(..., description='active/resolved')
    robot_identifier: str | None = None
    robot_token: str = Field(..., min_length=1)
