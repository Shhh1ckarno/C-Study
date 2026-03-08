from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  
    description = Column(String, nullable=False)
    answers = Column(JSON, nullable=False)

class UsersTasksSolved(Base):
    __tablename__ = "users_tasks"

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False,primary_key=True)
    task_id = Column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False,primary_key=True)
    