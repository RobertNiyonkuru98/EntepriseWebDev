# --------------------------
# Import required libraries
# --------------------------

# Import classes that allow us to create an HTTP server in Python
# BaseHTTPRequestHandler → handles incoming requests (GET, POST, etc.)
# HTTPServer → runs the server itself
from http.server import BaseHTTPRequestHandler, HTTPServer

# Import json module so we can send and receive data in JSON format
import json


# --------------------------
# Fake Database (In-Memory)
# --------------------------

# This list represents our "database"
# In real applications, this would be a database (MySQL, PostgreSQL, etc.)
trips = [
    {
        "id": 1,
        "passenger": "Uwimana",
        "pickup": "Kigali"
    },
    {
        "id": 2,
        "passenger": "Mugisha",
        "pickup": "Kigali"
    }
]


# --------------------------
# Request Handler Class
# --------------------------

# This class tells Python how to respond to HTTP requests
# Every request sent to the server is handled here
class SimpleHandler(BaseHTTPRequestHandler):
    """
    Handles incoming HTTP requests.
    Every time a client (browser, Postman, curl) calls our API,
    this class decides what response to send back.
    """

    # --------------------------
    # Helper Method for Headers
    # --------------------------
    def _set_headers(self, status=200):
        # Send an HTTP status code back to the client
        # 200 = OK, 404 = Not Found, etc.
        self.send_response(status)

        # Tell the client that our response is JSON data
        self.send_header("Content-Type", "application/json")

        # End the HTTP headers section
        self.end_headers()

    # --------------------------
    # Handle GET Requests
    # --------------------------
    def do_GET(self):
        # self.path contains the URL path the client requested
        # Example: "/trips"

        # If the client requests /trips
        if self.path == "/trips":
            # Set HTTP response headers (200 OK)
            self._set_headers()

            # Convert Python list (trips) into JSON
            # Encode it so it can be sent over the network
            # database, serialize, fetch->>>.
            self.wfile.write(json.dumps(trips).encode())

        else:
            # If the requested URL does not exist,
            # return a 404 Not Found error
            self._set_headers(404)

            # Send an error message in JSON format
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())


    def do_POST(self):

        if self.path == "/trips":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                newtrip = json.loads(body)
                trips.append(newtrip)

                self._set_headers(201)
                self.wfile.write(json.dumps({
                    "message": "Trip created",
                    "trip": newtrip
                }))
            except:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "error": "Invalid JSON"
                })).encode


    def do_DELETE(self):

        if self.path.startswith("/trips/"):
            try:
                trip_id = int(self.path.split("/")[-1])

                for trip in trips:
                    if trip["id"] == trip_id:
                        trips.remove(trip)

                        self._set_headers(200)

                        self.wfile.write(json.dumps({
                            "message": "trip deleted"
                        }).encode())
                        return
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    "error": "Trip not fonud"
                }).encode())

            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "error": "Invalid trip ID"
                }))




# --------------------------
# Run the Server
# --------------------------

def run(port=8000):
    """
    Starts the HTTP server on the given port.
    Port 8000 is commonly used for development.
    """

    # Create the server
    # "" means accept requests from any address (localhost)
    # SimpleHandler tells the server how to handle requests
    server = HTTPServer(("", port), SimpleHandler)

    # Print a message so we know the server is running
    print(f"Server running at http://localhost:{port}")

    # Keep the server running forever
    # (until we stop it with CTRL+C)
    server.serve_forever()


# --------------------------
# Program Entry Point
# --------------------------

# This ensures the server only starts when this file is run directly
# (and not when imported into another file)
if __name__ == "__main__":
    run()