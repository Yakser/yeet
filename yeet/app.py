from http.server import HTTPServer

from abc import ABC
from http.server import BaseHTTPRequestHandler
import re

from yeet.templating import render_template


class HTTPRequestHandler(BaseHTTPRequestHandler, ABC):
    app = None

    def do_GET(self):
        # fixme: routes order
        for route, controller in HTTPRequestHandler.app.url_map.items():
            self.path = self.path.lstrip('/')
            matches = re.match(route, self.path)
            if matches:
                if hasattr(controller, '__call__'):
                    self._send(controller().render(self.request, self.path), code=200)
                else:
                    self._send(controller.render(self.request, self.path), code=200)
                break
        else:
            self._send(render_template('404.html'), code=404)

    def _send(self, page, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(self._to_bytes(page))

    @staticmethod
    def _to_bytes(value):
        return bytes(value, encoding='utf-8')


class Yeet:
    _instance = None

    def __init__(self, name: str = 'app') -> None:
        self.name = name
        self.url_map = {}

    def run(self, host: str = '', port: int = 8080) -> None:
        if host == '':
            host = 'localhost'

        print(f"Starting {self.name} on {host}:{port}")
        server = HTTPServer((host, port), HTTPRequestHandler)
        print(f"Server has been started!")
        server.serve_forever()

    def add_route(self, path, controller):
        if path not in self.url_map:
            self.url_map[path] = controller
        else:
            raise ValueError(f"Route {path} already added!")

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        HTTPRequestHandler.app = cls._instance
        return cls._instance
