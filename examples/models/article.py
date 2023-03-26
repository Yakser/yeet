from python_yeet.orm import BaseModel, BaseManager


class Article(BaseModel):
    table_name = "articles"
    manager_class = BaseManager
