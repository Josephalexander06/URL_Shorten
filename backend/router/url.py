from fastapi import APIRouter, HTTPException, status, Depends
from utils import schema 
from utils.database import get_db
from sqlalchemy.orm import Session
import string
import hashlib
import models
from fastapi.responses import RedirectResponse

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
        arr.routerend(BASE62_ALPHA[rem])
    
    return "".join(reversed(arr))

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_url(url:schema.Create_Url,db:Session = Depends(get_db)):

    find_url = db.query(models.URL).filter(models.URL.original_url == url.org_url).first()

    if find_url:

        found_url = {
            "id":find_url.id,
            "original_url":find_url.original_url,
            "Shorten_url":find_url.shorten_url
        }

        return found_url

    url_slug = url_to_base62_hash(url.org_url)
    url.short_url = url_slug

    db_url = models.URL(
        original_url = url.org_url,
        shorten_url = url.short_url
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return url  

@router.get("/")
async def get_all_urls(db:Session=Depends(get_db)):
    get_url  = db.query(models.URL).all()

    if not get_url:
        raise HTTPException(status_code=404,detail="Not Found")
    return get_url

@router.get("/{short}")
def get_url(short:str,db:Session=Depends(get_db)):
    
    
    found_url  = db.query(models.URL).filter(models.URL.shorten_url == short).first()

    if not found_url:
        raise HTTPException(status_code=404,detail="Not found")

    redirect_url = found_url.original_url
    return RedirectResponse(url = redirect_url,status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    