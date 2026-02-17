from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory storage (like a fake database)
rides = []


class MotoTaxiHandler(BaseHTTPRequestHandler):

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # GET /rides
    def do_GET(self):
        if self.path == "/rides":
            self._send_response(200, rides)
        else:
            self._send_response(404, {"error": "Resource not found"})

    # POST /rides
    def do_POST(self):
        if self.path == "/rides":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                ride_data = json.loads(body)
                rides.append(ride_data)

                self._send_response(201, {
                    "message": "Ride created",
                    "ride": ride_data
                })

            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON"})
        else:
            self._send_response(404, {"error": "Resource not found"})


def run():
    server = HTTPServer(("localhost", 8000), MotoTaxiHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
