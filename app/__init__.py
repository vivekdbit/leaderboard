from flask import Flask
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth

mongo = PyMongo()
auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mongo.init_app(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
