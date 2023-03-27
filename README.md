# yeet
# [what's a yeet?](https://www.youtube.com/watch?v=fVva0bV0odg)

# quickstart

## Run app
```python
import os
from controllers import HomeController, ArticlesController
from examples.constants import INIT_QUERIES, DB_SETTINGS
from python_yeet.app import Yeet
from python_yeet.db import Database

app = Yeet(name=os.path.basename(os.getcwd()))
app.add_route(r'^articles/$', ArticlesController(methods=['GET', 'POST']))
app.add_route(r'^.*$', HomeController)
db = Database(db_settings=DB_SETTINGS,
              init_queries=INIT_QUERIES)
app.run()
```

## Create model example

```python
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
```

## Create controller example

```python
from examples.models.article import Article
from python_yeet.controllers import BaseController


class ArticlesController(BaseController):
    def get(self, path):
        return self.render_template('articles.html', articles=self._get_articles())
        
   
    @staticmethod
    def _get_articles():
        articles = Article.objects.select("id", "title")
        return articles
```
