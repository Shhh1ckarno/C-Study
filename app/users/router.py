from fastapi import APIRouter, Depends, HTTPException, Response
from app.users.auth import create_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUser
from app.config import Settings

router = APIRouter(prefix="/users", tags=["Авторизация и регистрация"])

@router.post("/register")
async def register(user_pass_email : SUser):
    user = await UsersDAO.get_one_or_none(email=user_pass_email.email)
    if user:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    hashed_password = get_password_hash(user_pass_email.hashed_password)
    await UsersDAO.add(email=user_pass_email.email, hashed_password=hashed_password)

@router.post("/login")
async def login(response: Response, user_pass_email : SUser):
    user = await UsersDAO.get_one_or_none(email=user_pass_email.email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not user.hashed_password == get_password_hash(user_pass_email.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    
    access_token = create_token(data={"sub": user.id,
                                        "role": user.role}, 
                                        expire_minutes=Settings.access_token_expire_minutes)
    refresh_token = create_token(data={"sub": user.id,
                                        "role": user.role},
                                        expire_minutes=Settings.refresh_token_expire_minutes)
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

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    