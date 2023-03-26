import os

from controllers import HomeController, ArticlesController, ArticleDetailController
from examples.constants import INIT_QUERIES, DB_SETTINGS
from python_yeet.app import Yeet
from python_yeet.db import Database

if __name__ == '__main__':
    app = Yeet(name=os.path.basename(os.getcwd()))

    app.add_route(r'^articles/(\d+)/$', ArticleDetailController(methods=['GET', 'PUT']))
    app.add_route(r'^articles/$', ArticlesController(methods=['GET', 'POST']))
    app.add_route(r'^.*$', HomeController)

    db = Database(db_settings=DB_SETTINGS,
                  init_queries=INIT_QUERIES)

    app.run()
