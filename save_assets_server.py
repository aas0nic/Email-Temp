import http.server
import socketserver
import json
import base64
import os

PORT = 8765
DIRECTORY = "/Users/itz_ats_sama/Email Temp"

class AssetHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            assets = json.loads(post_data.decode('utf-8'))
            for filename, data_url in assets.items():
                if data_url.startswith('data:image/png;base64,'):
                    base64_data = data_url.split(',', 1)[1]
                    file_bytes = base64.b64decode(base64_data)
                    file_path = os.path.join(DIRECTORY, filename)
                    with open(file_path, 'wb') as f:
                        f.write(file_bytes)
                    print(f"Saved: {filename} ({len(file_bytes)} bytes)")
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"OK")
            print("All assets saved successfully!")
            import threading
            threading.Timer(1.0, self.server.shutdown).start()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AssetHandler) as httpd:
        print(f"Serving asset generator at http://127.0.0.1:{PORT}")
        httpd.serve_forever()
