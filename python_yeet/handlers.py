import re
from abc import ABC
from http.server import BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler, ABC):
    app = None

    def do_GET(self):
        self._process_request('GET')

    def do_POST(self):
        self._process_request('POST')

    def do_PUT(self):
        self._process_request('PUT')

    def _process_request(self, method):
        for route, controller in HTTPRequestHandler.app.url_map.items():
            print(method, controller.methods)
            if method in controller.methods:
                self.path = self.path.lstrip('/')
                matches = re.fullmatch(re.compile(route), self.path)
                if matches:
                    rendered_page = controller.render(self.request, self.path, *matches.groups())
                    self._send(rendered_page, code=200)
                    break
        else:
            self._send('', code=404)

    def _send(self, page, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")

        page = self._to_bytes(page)
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    @staticmethod
    def _to_bytes(value):
        return value.encode("utf-8")
