from examples.models.article import Article
from python_yeet.controllers import BaseController
from urllib.parse import parse_qs


class HomeController(BaseController):
    def get(self, path):
        return self.render_template('home.html')


class ArticlesController(BaseController):
    def _get_articles(self):
        articles = Article.objects.select("id", "title")
        return articles

    def post(self, path):
        article = Article.objects.create(title="New article", text="new newn ewnewnwe", author=1)
        return str(article)

    def get(self, path):
        return self.render_template('articles.html', articles=self._get_articles())


class ArticleDetailController(BaseController):
    def _get_article(self, id):
        return Article.objects.get(id)

    def get(self, path, id):
        return self.render_template('article.html', article=self._get_article(id))


class ArticleDeleteController(BaseController):
    def _get_article(self, id):
        return Article.objects.get(id)

    def post(self, path, id):
        article = Article.objects.delete(id)
        return self.render_template('article_delete.html', article=article)

    def get(self, path, id):
        return self.render_template('article_delete.html', article=self._get_article(id))


class ArticleEditController(BaseController):
    def _get_article(self, id):
        return Article.objects.get(id)

    def _update_article(self, id, data):
        Article.objects.update(id, data)

    def post(self, path, id, data):
        self._update_article(id, data)
        return self.render_template('article_edit.html', article=self._get_article(id))

    def get(self, path, id):
        return self.render_template('article_edit.html', article=self._get_article(id))
