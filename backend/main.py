from fastapi import FastAPI
from utils import schema
import string,random
import hashlib

app =  FastAPI()

@app.get("/")
async def root():
    return {"msg":"Started Project"} 

BASE62_ALPHA = string.digits + string.ascii_letters

def url_to_base62_hash (url:str)-> str:

    hasher =  hashlib.md5(url.encode('utf-8'))

    url_int = int(hasher.hexdigest()[:16],16)
    
    arr = []
    base = len(BASE62_ALPHA)
    while url_int > 0:
        url_int , rem = divmod(url_int, base)
        arr.append(BASE62_ALPHA[rem])
    
    return "".join(reversed(arr))

@app.post("/url")
async def create_url(url:schema.Url):
    url_slug = url_to_base62_hash(url.org_url)
    url.short_url = url_slug

    return url  
    
