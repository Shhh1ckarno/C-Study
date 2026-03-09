from app.dao.base import BaseDAO
from app.tasks.models import Tasks
from app.tasks.schemas import STaskCreate
from app.database import async_sessionmaker
from sqlalchemy import delete


class TasksDAO(BaseDAO):
    model = Tasks

    @classmethod
    async def add_task(cls, data : STaskCreate):
        task_dict = data.model_dump()
        await cls.add(**task_dict)
    
    @classmethod
    async def delete_task(cls, task_id: int):
        async with async_sessionmaker() as session:
            query = delete(cls.model).where(cls.model.id == task_id)
            await session.execute(query)
            await session.commit()
    