from app.dao.base import BaseDAO
from app.tasks.models import Tasks, UsersTasksSolved
from app.tasks.schemas import STaskCreate
from app.database import async_sessionmaker
from sqlalchemy import delete


class TasksDAO(BaseDAO):
    model = Tasks

    @classmethod
    async def add_task(cls, data : STaskCreate):
        task_dict = data.model_dump()
        await cls.add(**task_dict)

class UsersTasksSolvedDAO(BaseDAO):
    model = UsersTasksSolved
    
    
    