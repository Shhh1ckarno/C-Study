from sqlalchemy import insert, select
from app.database import async_sessionmaker, Base

class BaseDAO():
    model = None

    @classmethod
    async def get_one_or_none(cls, **kwargs):
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.model).filter_by(**kwargs)
            )
            return query.scalars().one_or_none()
    
    @classmethod
    async def add(cls, **kwargs):
        async with async_sessionmaker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()
    