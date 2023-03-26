from examples.models.article import Article
from python_yeet.controllers import BaseController


class HomeController(BaseController):
    def render(self, request, path):
        return self.render_template('home.html')


class ArticlesController(BaseController):
    def _get_articles(self):
        articles = Article.objects.select("id", "title")
        return articles

    def render(self, request, path):
        return self.render_template('articles.html', articles=self._get_articles())


class ArticleDetailController(BaseController):
    def _get_article(self, id):
        return Article.objects.get(id, "title", "text")

    def render(self, request, path, id):
        return self.render_template('article.html', article=self._get_article(id))
