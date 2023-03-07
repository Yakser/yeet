from jinja2 import Environment, PackageLoader, select_autoescape, Template

env = Environment(
    loader=PackageLoader('examples', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render_template(template_name: str, **context):
    template = env.get_or_select_template(template_name)
    return template.render(context)
