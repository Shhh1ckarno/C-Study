from sqlalchemy import String, cast, select, update

from app.dao.base import BaseDAO
from app.tasks.dao import TasksDAO
from app.topics.models import Topics
from app.database import async_sessionmaker


class TopicsDAO(BaseDAO):
    model = Topics
    @classmethod
    async def add_task_into_topic(cls, topic_id: int, task_id: int):
        topic = await cls.get_one_or_none(id=topic_id)
        if not topic:
            return None
        current_tasks = list(topic.tasks_ids) if topic.tasks_ids else []

        if task_id not in current_tasks:
            current_tasks.append(task_id)
            async with async_sessionmaker() as session:
                query = (
                update(cls.model).where(cls.model.id == topic_id).values(tasks_ids=current_tasks)
                )
                await session.execute(query)
                await session.commit()
                
            return current_tasks
    @classmethod
    async def get_tasks_from_topic(cls, topic_id: int):
        topic = await cls.get_one_or_none(id=topic_id) 
        if not topic or not topic.tasks_ids:
            return []

        all_tasks = []
        for task_id in topic.tasks_ids:
            task = await TasksDAO.get_one_or_none(id=task_id)
            if task:
                all_tasks.append(task) 
        return all_tasks
    
    @classmethod
    async def find_topics_by_task(cls, task_id: int):
        async with async_sessionmaker() as session:
            target = f'%{task_id}%'
            query = select(cls.model).where(
                cast(cls.model.tasks_ids, String).like(target)
            )
            result = await session.execute(query)
            res = result.scalars().one_or_none()
            print(f"DEBUG: Search task {task_id} in topics. Result: {res}") 
            return res
