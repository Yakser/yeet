from abc import ABC, abstractmethod


class BaseController(ABC):
    def __init__(self, jinja_env=None):
        super().__init__()
        self.jinja_env = jinja_env

    @abstractmethod
    def render(self, request, path):
        pass

    def render_template(self, template_name: str, **context):
        template = self.jinja_env.get_or_select_template(template_name)
        return template.render(context)
