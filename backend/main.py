from fastapi import FastAPI
from functools import lru_cache
from database import engine
import models
from router import url,users
from core.config import settings

app =  FastAPI()

models.Base.metadata.create_all(bind=engine)

@lru_cache
def get_settings():
    return settings()

app.include_router(url.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"msg":"Started Project"} 
