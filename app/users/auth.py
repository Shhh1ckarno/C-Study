from datetime import datetime, timedelta, timezone
import hashlib
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from app.config import settings
from app.users.dao import UsersDAO
from jose import ExpiredSignatureError, JWTError, jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    utf8_password = password.encode('utf-8')
    sha256_hash = hashlib.sha256(utf8_password).hexdigest() 
    return pwd_context.hash(sha256_hash)

def verify_password(plain_password:str, hashed_password:str)->bool:
    utf8_password = plain_password.encode('utf-8')
    sha256_hash = hashlib.sha256(utf8_password).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)

async def authentificate_user(email : EmailStr, password:str):
    user = await UsersDAO.get_one_or_none(email=email)
    if not user or not verify_password(password,user.hashed_password):
        return None
    return user 

def create_token(data:dict, expire_minutes: int = None)->str:
    key=settings.SECRET_KEY
    alg=settings.alg
    to_encode=data.copy()
    if expire_minutes is None:
        expire_minutes = settings.access_token_expire_minutes
    expire=datetime.now(timezone.utc)+timedelta(minutes=expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, key, alg)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.alg])
        return payload
    except ExpiredSignatureError:
        print("DEBUG: Срок действия токена истек (ExpiredSignatureError)")
        return None 
    except JWTError as e:
        print(f"DEBUG: Критический сбой JWT: {e}")
        raise HTTPException(status_code=401, detail="Невалидный токен")
    
    