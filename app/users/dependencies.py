from fastapi import Depends, HTTPException, Request, Response

from app.config import Settings
from app.users.auth import create_token, decode_token


def get_accesstoken(request: Request):
    return request.cookies.get("access_token")

def get_refreshtoken(request: Request):
    return request.cookies.get("refresh_token")

def get_current_decoded_token(response: Response, access_token:str = Depends(get_accesstoken()), refresh_token:str = Depends(get_refreshtoken())):
    if not access_token:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Нет токена доступа")
        else:
            decoded_refresh_token = decode_token(refresh_token)
            if not decoded_refresh_token:
                raise HTTPException(status_code=401, detail="Невалидный токен обновления")
            new_access_token = create_token(data={"sub": decoded_refresh_token["sub"],
                                                "role": decoded_refresh_token["role"]},
                                                expire_minutes=Settings.access_token_expire_minutes)
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True
            )
            return decoded_refresh_token
            



