from fastapi import FastAPI
from utils.database import engine
import models
from router import url


app =  FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(url.router)

@app.get("/")
async def root():
    return {"msg":"Started Project"} 
