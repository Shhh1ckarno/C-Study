from sqlalchemy import Column, Integer, String
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password=Column(String)
    role = Column(String, default="user")


