import re
from abc import ABC
from http.server import BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler, ABC):
    app = None

    def do_GET(self):
        # fixme: routes order
        for route, controller in HTTPRequestHandler.app.url_map.items():
            self.path = self.path.lstrip('/')
            matches = re.fullmatch(re.compile(route), self.path)
            if matches:
                self._send(controller.render(self.request, self.path, *matches.groups()), code=200)
                break
        else:
            self._send('', code=404)

    def _send(self, page, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(self._to_bytes(page))

    @staticmethod
    def _to_bytes(value):
        return bytes(value, encoding='utf-8')
