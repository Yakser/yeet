from yeet.controllers import BaseController
from yeet.templating import render_template


class HomeController(BaseController):
    def render(self, request, path):
        return render_template('base.html', data='this is home')


class ProfileController(BaseController):
    def render(self, request, path):
        return render_template('base.html', data='this is profile')
