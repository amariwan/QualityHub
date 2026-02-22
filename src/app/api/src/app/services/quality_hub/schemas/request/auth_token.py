from pydantic import BaseModel, Field


class ConnectTokenRequest(BaseModel):
    token: str = Field(min_length=1)
    base_url: str | None = None
