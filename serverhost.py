from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import os
import requests  # Ensure you have the requests library installed

class LoginHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                # Ensure the file path is correct
                script_dir = os.path.dirname(__file__)
                file_path = os.path.join(script_dir, 'login.html')
                print(f"Looking for file: {file_path}")  # Debugging line
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
                print("Served login.html")
            except Exception as e:
                print(f"Error serving login.html: {e}")
                self.send_error(500, "Internal Server Error")
        else:
            print(f"404 Not Found: {self.path}")  # Debugging line
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/auth':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))

            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            license = params.get('license', [''])[0]

            # Perform KeyAuth authentication here
            response = self.authenticate_with_keyauth(username, password, license)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

    def authenticate_with_keyauth(self, username, password, license):
        # KeyAuth API setup (ensure to replace with actual API details)
        api_url = "https://api.keyauth.cc/api/validate"  # KeyAuth API endpoint
        data = {
            "username": username,
            "password": password,
            "license": license,
            "hash_to_check": self.getchecksum(),  # Replace with actual checksum logic
        }

        try:
            response = requests.post(api_url, json=data)
            result = response.json()

            if result.get("status") == "success":
                return {"status": "success", "message": "Logged in successfully"}
            else:
                return {"status": "failure", "message": "Invalid credentials"}
        except Exception as e:
            return {"status": "failure", "message": f"Error with KeyAuth API: {str(e)}"}

    def getchecksum(self):
        # Implement your checksum logic here
        return "your_checksum_here"  # Replace with actual checksum logic

def run(server_class=HTTPServer, handler_class=LoginHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
