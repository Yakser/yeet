import datetime

from python_yeet.orm import BaseModel, BaseManager


class Article(BaseModel):
    table_name = "articles"
    manager_class = BaseManager

    id: int
    title: str
    text: str
    author: int
    created_at: datetime.datetime
