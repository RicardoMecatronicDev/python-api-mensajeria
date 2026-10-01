from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str
    to: str
    from_: str = Field(alias="from")
    timeToLifeSec: int = Field(gt=0)  # noqa: N815
