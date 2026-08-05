from fastapi import FastAPI
from functools import lru_cache
from utils.database import engine
import models
from router import url
from utils.config import Settings

app =  FastAPI()

models.Base.metadata.create_all(bind=engine)

@lru_cache
def get_settings():
    return Settings()

app.include_router(url.router)

@app.get("/")
async def root():
    return {"msg":"Started Project"} 
