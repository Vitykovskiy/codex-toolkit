import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/contact":
            self.send_error(404)
            return
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        status, data = 201, {"id": "contact-1"}
        if not payload.get("name") or not payload.get("email"):
            status, data = 422, {"message": "Name and email required"}
        elif payload["email"] == "fail@example.test":
            status, data = 422, {"message": "Email rejected"}
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
