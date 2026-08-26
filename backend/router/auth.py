from fastapi import Security,Depends,HTTPException,status
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id") 


        if username is None or user_id is None:
            raise credentials_exception
        return user_id

    except JWTError:
        raise HTTPException(status_code=404,detail="Invalid credentials")