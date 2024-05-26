from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

# In-memory user store for basic authentication
users = {
    "admin": "password"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username