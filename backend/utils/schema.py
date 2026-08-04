from pydantic import BaseModel


class Create_Url(BaseModel):
    org_url : str
    short_url : str | None = None
    
    class Config:
        from_attribute = True