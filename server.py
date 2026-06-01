#!/usr/bin/env python3
import sys, os, json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
REC_DIR = os.path.join(ROOT, 'recordings')
os.makedirs(REC_DIR, exist_ok=True)

def safe_name(name):
    return name and '/' not in name and '\\' not in name and '..' not in name

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/save':
            qs = parse_qs(parsed.query)
            name = qs.get('name', [''])[0]
            if not safe_name(name):
                self.send_error(400, 'bad name'); return
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            with open(os.path.join(REC_DIR, name), 'wb') as f:
                f.write(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True}).encode())
        else:
            self.send_error(404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path == '/delete':
            qs = parse_qs(parsed.query)
            name = qs.get('name', [''])[0]
            if not safe_name(name):
                self.send_error(400); return
            p = os.path.join(REC_DIR, name)
            if os.path.exists(p): os.remove(p)
            self.send_response(200); self.end_headers()
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(ROOT)
    print(f"Serving {ROOT} on http://localhost:{port}/")
    HTTPServer(('', port), Handler).serve_forever()
