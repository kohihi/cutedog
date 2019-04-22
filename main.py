from app import app
from routes.index import main as route_index
from routes.api import main as route_api

app.register_blueprint(route_index)
app.register_blueprint(route_api, url_prefix='/api')

if __name__ == "__main__":
    app.run(
        port=9001,
        host="127.0.0.1",
        debug=True,
    )
