from utils import database
from fastapi import APIRouter, HTTPException, status, Depends,Request
from utils import schema 
from utils.database import get_db
from sqlalchemy.orm import Session
import string
import hashlib
import models
from fastapi.responses import RedirectResponse
import time
from datetime import datetime, timezone, timedelta
from user_agents import parse


router = APIRouter(
    prefix="/url",
    tags=["urls"]
)


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

def find_ip_address(request):

    x_forward_for = request.headers.get("x-forwarded-for")
    if x_forward_for:
        client_ip = x_forward_for.split(",")[0].strip()
    elif request.client:
        client_ip = request.client.host
    else:
        client_ip = None
    
    return client_ip

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_url(url:schema.Create_Url,request:Request,db:Session = Depends(get_db)):

    reserved_words = ["docs","admin","url","redoc"]
        
    client_ip = find_ip_address(request)
    info = request.headers.get("User-Agent", "")
    user_agent = parse(info)

    ua = ", ".join([
        user_agent.browser.family,
        user_agent.os.family
    ])
    expire = datetime.now(timezone.utc) + timedelta(days=7)

    if url.custom_url:
    
        if url.custom_url.lower() in reserved_words:

            raise HTTPException(status_code=400,detail="Custom url reserved words cant use")

        check_custom_url = db.query(models.URL).filter(models.URL.shorten_url == url.custom_url).first()

        if check_custom_url:
            raise HTTPException(status_code=409,detail="Custom url already exists")

        db_url = models.URL(
            original_url = str(url.org_url),
            shorten_url = url.custom_url,
            ip_address = client_ip,
            user_agent_info = ua,
            expire_at = expire,
            count = 1
            )

        db.add(db_url)
        db.commit()
        db.refresh(db_url)

        return db_url  


    find_url = db.query(models.URL).filter(models.URL.original_url == str(url.org_url)).first()

    if find_url:

        found_url = {
            "id":find_url.id,
            "original_url":find_url.original_url,
            "shorten_url":find_url.shorten_url
        }

        return found_url
    
    
    url_slug = url_to_base62_hash(str(url.org_url))

    while db.query(models.URL).filter(models.URL.shorten_url == url_slug).first():
          url_slug = url_to_base62_hash(str(url.org_url) + str(time.time()))
    

    db_url = models.URL(
        original_url = str(url.org_url),
        shorten_url = url_slug,
        ip_address = client_ip,
        user_agent_info = ua,
        expire_at = expire,
        count = 1
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url  


@router.get("/")
async def get_all_urls(db:Session=Depends(get_db)):
    get_url  = db.query(models.URL).all()

    if not get_url:
        raise HTTPException(status_code=404,detail="Not Found")
    return get_url


@router.get("/{short}")
def get_url(short:str,request: Request,db:Session=Depends(get_db)):
    
    
    found_url  = db.query(models.URL).filter(models.URL.shorten_url == short).first()

    if not found_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found")
    
    if found_url.expire_at and datetime.now(timezone.utc) > found_url.expire_at:
        db.delete(found_url)
        db.commit()
        raise HTTPException(status_code=404,detail="Item has been expired")
    
    client_ip = find_ip_address(request)
    info = request.headers.get("User-Agent", "")
    user_agent = parse(info)

    ua = ", ".join([
        user_agent.browser.family,
        user_agent.os.family
    ])
    
    found_url.count = found_url.count + 1
    found_url.ip_address = client_ip
    found_url.access_at =datetime.now()
    found_url.user_agent_info = ua

    db.add(found_url)
    db.commit()


    redirect_url = found_url.original_url
    return RedirectResponse(url = redirect_url,status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    