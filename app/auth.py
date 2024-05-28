from flask_httpauth import HTTPBasicAuth
from app.config import Config

auth = HTTPBasicAuth()

#basic authentication
users = {
    Config.API_AUTH_USERNAME: Config.API_AUTH_PASSWORD
}

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username