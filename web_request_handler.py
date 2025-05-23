import json

from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        print("==========================")
        print(f"PATH: {self.url.path}")
        print(f"QUERY_DATA: {self.query_data}")
        post_json = json.loads(self.post_data.decode("utf-8")) if self.post_data else {}
        print(f"POST_DATA: {self.post_data.decode('utf-8')}")
        print(f"POST_JSON: {post_json}")
        print(f"FORM_DATA: {self.form_data}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(self.get_response(post_json.get("message").get("chat").get("id")).encode("utf-8"))

    def do_POST(self):
        self.do_GET()

    def get_response(self, chat_id, text="Got it!"):
        return json.dumps(
            {
                "path": self.url.path,
                "query_data": self.query_data,
                "post_data": self.post_data.decode("utf-8"),
                "form_data": self.form_data,
                "cookies": {
                    name: cookie.value
                    for name, cookie in self.cookies.items()
                },
                "method": "sendMessage",
                "text": text,
                "chat_id": chat_id,
            }
        )