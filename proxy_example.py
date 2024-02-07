import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def do_PUT(self):
        self.proxy_request()

    def do_DELETE(self):
        self.proxy_request()

    def proxy_request(self):
        # Get the request data
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)

        # Modify the request body as needed
        modified_request_data = modify_request_body(request_data)

        # Make the request to the target server
        target_url = 'http://target-server.com' + self.path
        response = requests.request(self.command, target_url, data=modified_request_data, headers=self.headers)

        # Send the response from the target server back to the client
        self.send_response(response.status_code)
        for header, value in response.headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.content)

def run_proxy_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ProxyHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy_server()

def modify_request_body(request_data):
    # Modify the request body here
    modified_request_data = request_data.upper()

    return modified_request_data
