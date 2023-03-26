from abc import ABC, abstractmethod


class BaseController(ABC):
    def __init__(self, methods=None, jinja_env=None):
        super().__init__()
        self.jinja_env = jinja_env
        if methods is None:
            self.methods = ['GET']
        else:
            self.methods = methods.copy()

    @abstractmethod
    def render(self, request, path):
        pass

    def render_template(self, template_name: str, **context):
        template = self.jinja_env.get_or_select_template(template_name)
        return template.render(context)
