from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import Optional

class Create_Url(BaseModel):
    org_url : HttpUrl
    custom_url : Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$"
    )
    
    class Config:
        from_attribute = True

class User(BaseModel):
    email : EmailStr
    password : str = Field(
        min_length=6
    )
