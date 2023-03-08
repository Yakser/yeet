from http.server import HTTPServer

from jinja2 import Environment, PackageLoader, select_autoescape

from python_yeet.handlers import HTTPRequestHandler


class Yeet:
    _instance = None

    def __init__(self, name: str = 'examples') -> None:
        self.name = name
        self.url_map = {}

        self.jinja_env = Environment(
            loader=PackageLoader(self.name, 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def run(self, host: str = '', port: int = 8080) -> None:
        if host == '':
            host = 'localhost'

        print(f"Starting {self.name} on {host}:{port}")
        server = HTTPServer((host, port), HTTPRequestHandler)
        print(f"Server has been started!")
        server.serve_forever()

    def add_route(self, path, controller):
        if path not in self.url_map:
            if hasattr(controller, '__call__'):
                controller = controller(jinja_env=self.jinja_env)
            else:
                controller = controller.__class__(jinja_env=self.jinja_env)
            self.url_map[path] = controller

        else:
            raise ValueError(f"Route {path} already added!")

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        HTTPRequestHandler.app = cls._instance
        return cls._instance