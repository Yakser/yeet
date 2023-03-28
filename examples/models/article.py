import datetime

from python_yeet.orm import BaseModel


class Article(BaseModel):
    table_name = "articles"

    id: int
    title: str
    text: str
    author: int
    created_at: datetime.datetime
