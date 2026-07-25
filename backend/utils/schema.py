from pydantic import BaseModel


class Url(BaseModel):
    org_url : str
    short_url : str | None = None
