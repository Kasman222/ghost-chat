from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import urllib.parse
import os

PAGE = (Path(__file__).parent / "index.html").read_bytes()


class Handler(BaseHTTPRequestHandler):

    def _send(self, code, body=b"", ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif path == "/health":
            self._send(200, b"OK")
        else:
            self._send(404, b"Not found")

    do_HEAD = do_GET

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path != "/word":
            self._send(404, b"Not found")
            return

        length = min(int(self.headers.get("Content-Length", 0)), 10000)
        data = self.rfile.read(length).decode("utf-8", errors="replace")
        info = urllib.parse.parse_qs(data)

        username = info.get("user", [""])[0][:60]
        message = info.get("word", [""])[0][:300]

        # Shows up in the Render "Logs" tab
        print(f"NEW MESSAGE -> {username}: {message}", flush=True)

        self._send(200, b"OK")


port = int(os.environ.get("PORT", 8080))
server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
print("Server running on port", port, flush=True)
server.serve_forever()
