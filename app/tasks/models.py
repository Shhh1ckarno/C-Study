from sqlalchemy import JSON, Column, Integer, String
from app.database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  
    description = Column(String, nullable=False)
    answers = Column(JSON, nullable=False)