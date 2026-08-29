from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
from database import engine
import models
from router import url,users
from core.config import settings

app =  FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@lru_cache
def get_settings():
    return settings()

app.include_router(url.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"msg":"Started Project"} 
