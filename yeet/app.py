from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable


class BaseRequestHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests by returning a fixed 'page'
    Args:
        BaseHTTPRequestHandler (_type_): _description_
    """

    PAGE = '''\
<html>
<body>
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>
'''

    @staticmethod
    def to_bytes(value):
        return bytes(value, encoding='utf-8')

    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):
        values = {
            "date_time": self.date_time_string(),
            "client_host": self.client_address[0],
            "client_port": self.client_address[1],
            "command": self.command,
            "path": self.path
        }

        page = self.PAGE.format(**values)

        return page

    def send_page(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(self.to_bytes(page))


class Yeet:
    _instance = None

    def __init__(self, name: str = 'app') -> None:
        self.name = name

    def run(self, host: str = '', port: int = 8080) -> None:
        server = HTTPServer((host, port), BaseRequestHandler)
        server.serve_forever()

    def route(self, rule: str, **options: Any) -> Callable:
        """Decorate a view function to register it with the given URL
        rule and options. Calls :meth:`add_url_rule`, which has more
        details about the implementation.
        .. code-block:: python
            @app.route("/")
            def index():
                return "Hello, World!"
        See :ref:`url-route-registrations`.
        The endpoint name for the route defaults to the name of the view
        function if the ``endpoint`` parameter isn't passed.
        The ``methods`` parameter defaults to ``["GET"]``. ``HEAD`` and
        ``OPTIONS`` are added automatically.
        :param rule: The URL rule string.
        :param options: Extra options passed to the
            :class:`~werkzeug.routing.Rule` object.
        """

        def decorator(f: str) -> str:
            endpoint = options.pop("endpoint", None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f

        return decorator

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
