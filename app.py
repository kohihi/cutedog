from flask import Flask
from config import settings
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO

db = MongoEngine()
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(settings[config_name])

    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'
    from routes.api import main as route_api
    from routes.index import main as route_index
    from routes.events import main as route_socket
    app.register_blueprint(route_index, url_prefix="/")
    app.register_blueprint(route_api, url_prefix="/api")
    app.register_blueprint(route_socket)

    db.init_app(app)
    socketio.init_app(app)

    return app
