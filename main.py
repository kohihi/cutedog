from app import app

from routes.events import socketio
from routes.api import main as route_api
from routes.index import main as route_index
from routes.events import main as route_socket
app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_api, url_prefix="/api")
app.register_blueprint(route_socket)
socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app.run(
        port=9001
    ))
