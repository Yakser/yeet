from abc import ABC, abstractmethod

from python_yeet.helpers import clean_method


class BaseController(ABC):
    def __init__(self, methods=None, jinja_env=None):
        super().__init__()
        self.jinja_env = jinja_env
        if methods is None:
            self.methods = ['get']
        else:
            self.methods = methods.copy()

        self.methods = self._clean_methods(self.methods)

    @abstractmethod
    def get(self, path):
        pass

    def render_template(self, template_name: str, **context):
        template = self.jinja_env.get_or_select_template(template_name)
        return template.render(context)

    @staticmethod
    def _clean_methods(methods):
        return [clean_method(method) for method in methods]
