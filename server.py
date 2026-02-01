import http.server
import socketserver
import json
from datetime import datetime
from tools.console import info, warning, error

class LogHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/log":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                log_data = json.loads(post_data.decode('utf-8'))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                info(f"[{timestamp}] {log_data['level'].upper()}: {log_data['message']}")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"message": "Log server is running"}')
        else:
            self.send_response(404)
            self.end_headers()


with socketserver.TCPServer(("127.0.0.1", 8000), LogHandler) as httpd:
    warning("HTTP server started on http://127.0.0.1:8000")
    httpd.serve_forever()
