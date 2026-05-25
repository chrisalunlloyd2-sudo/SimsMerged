from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class API:
    def __init__(self, db):
        self.db = db

    def start(self):
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, RequestHandler)
        print("API server started on port 8000")
        httpd.serve_forever()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/sims":
            sims = self.server.db.get_sims()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(str(sims).encode())
        else:
            self.send_response(404)
            self.end_headers()
```

[CMD]
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/chrisalunlloyd2-sudo/SimsMerged.git
git push -u origin master
