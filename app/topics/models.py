
from sqlalchemy import JSON, Column, Integer, String

from app.database import Base


class Topics(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    tasks_ids = Column(JSON, nullable=False)

    