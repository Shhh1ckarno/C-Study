from app.dao.base import BaseDAO
from app.topics.models import Topics


class TopicsDAO(BaseDAO):
    model = Topics