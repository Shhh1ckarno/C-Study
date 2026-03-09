from fastapi import Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from jose import JWTError
from app.config import settings
from app.users.auth import create_token, decode_token
from app.users.dao import UsersDAO

templates = Jinja2Templates(directory="app/templates")

def get_accesstoken(request: Request):
    return request.cookies.get("access_token")

def get_refreshtoken(request: Request):
    return request.cookies.get("refresh_token")

def get_current_decoded_token(response: Response, access_token:str = Depends(get_accesstoken), refresh_token:str = Depends(get_refreshtoken)):
    if access_token:
        decoded_access = decode_token(access_token)
        if decoded_access:
            return decoded_access
        
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Сессия истекла, войдите снова")
    
    decoded_refresh = decode_token(refresh_token)
    if not decoded_refresh:
        raise HTTPException(status_code=401, detail="Невалидный refresh токен")

    new_access_token = create_token(
        data={"sub": str(decoded_refresh["sub"]), "role": str(decoded_refresh["role"])},
        expire_minutes=settings.access_token_expire_minutes
    )
    
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True
    )
    
    return decoded_refresh

async def get_current_user(decoded_token: dict = Depends(get_current_decoded_token)):
    user = await UsersDAO.get_one_or_none(id=int(decoded_token["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

async def get_current_user_optional(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = decode_token(token)
        if not payload:
            return None
            
        user_id = payload.get("sub")
        if not user_id:
            return None
            
        user = await UsersDAO.get_one_or_none(id=int(user_id))
        return user
        
    except (JWTError, Exception):
        return None



