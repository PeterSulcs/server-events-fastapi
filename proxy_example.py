from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Get the request data
    request_data = request.get_data()

    # Modify the request body as needed
    modified_request_data = modify_request_body(request_data)

    # Make the request to the target server
    target_url = 'http://target-server.com/' + path
    response = requests.request(request.method, target_url, data=modified_request_data, headers=request.headers)

    # Return the response from the target server
    return response.content, response.status_code, response.headers.items()

def modify_request_body(request_data):
    # Modify the request body here
    modified_request_data = request_data.upper()

    return modified_request_data

if __name__ == '__main__':
    app.run()
