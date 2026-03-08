from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from app.config import Settings
from app.users.dao import UsersDAO
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

async def authentificate_user(email : EmailStr, password:str):
    user = await UsersDAO.get_one_or_none(email=email)
    if not user or not verify_password(password,user.hashed_password):
        return None
    return user 

def create_token(data:dict, expire_minutes: int = None)->str:
    key=Settings.SECRET_KEY
    alg=Settings.alg
    to_encode=data.copy()
    if expire_minutes is None:
        expire_minutes = Settings.access_token_expire_minutes
    expire=datetime.now(timezone.utc)+timedelta(minutes=expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, key, alg)
    return encoded_jwt
    
    