from yeet.controllers import BaseController


class HomeController(BaseController):
    def render(self, request, path):
        return self.render_template('base.html', data='this is home')


class ProfileController(BaseController):
    def render(self, request, path):
        return self.render_template('base.html', data='this is profile')
