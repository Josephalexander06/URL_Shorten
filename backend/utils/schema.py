from pydantic import BaseModel, HttpUrl


class Create_Url(BaseModel):
    org_url : str = HttpUrl
    short_url : str | None = None
    
    class Config:
        from_attribute = True