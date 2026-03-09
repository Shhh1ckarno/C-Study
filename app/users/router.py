from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from app.users.auth import create_token, get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.users.schemas import SUser
from app.config import settings

router = APIRouter(prefix="/users", tags=["Авторизация и регистрация"])

@router.post("/register")
async def register(user_pass_email : SUser):
    user = await UsersDAO.get_one_or_none(email=user_pass_email.email)
    if user:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    hashed_password = get_password_hash(user_pass_email.password)
    await UsersDAO.add(email=user_pass_email.email, hashed_password=hashed_password)

@router.post("/login")
async def login(response: Response, user_pass_email : SUser):
    user = await UsersDAO.get_one_or_none(email=user_pass_email.email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not verify_password(user_pass_email.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    
    access_token = create_token(data={"sub": str(user.id),
                                        "role": user.role}, 
                                        expire_minutes=settings.access_token_expire_minutes)
    refresh_token = create_token(data={"sub": str(user.id),
                                        "role": user.role},
                                        expire_minutes=settings.refresh_token_expire_minutes)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True
    )

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/auth", status_code=303)
    response.set_cookie(
        key="access_token", 
        value="", 
        max_age=0, 
        expires=0, 
        path="/",
        httponly=True 
    )
    response.set_cookie(key="refresh_token", value="", max_age=0, expires=0, path="/")
    
    return response

