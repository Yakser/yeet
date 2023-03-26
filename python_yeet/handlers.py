import re
from abc import ABC
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from python_yeet.helpers import clean_method, clean_data


class HTTPRequestHandler(BaseHTTPRequestHandler, ABC):
    app = None

    def do_GET(self):
        self._process_request('GET')

    def do_POST(self):
        self._process_request('POST')

    def do_PUT(self):
        self._process_request('PUT')

    def _process_request(self, method):
        method = clean_method(method)
        for route, controller in HTTPRequestHandler.app.url_map.items():
            if method in controller.methods:
                self.path = self.path.lstrip('/')
                matches = re.fullmatch(re.compile(route), self.path)
                if matches:
                    if method == 'post':
                        content_length = int(self.headers['Content-Length'])
                        data = self.rfile.read(content_length)
                        data = parse_qs(data.decode("utf-8"), keep_blank_values=True)
                        response = controller.post(self.path, *matches.groups(), clean_data(data))
                    else:
                        response = getattr(controller, method)(self.path, *matches.groups())
                    self._send(response, code=200)
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
