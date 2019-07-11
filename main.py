from app import create_app, socketio
from os import getenv

app = create_app(getenv("ENV_KOHI", "dev"))

if __name__ == "__main__":
    socketio.run(app.run(
        port=9001
    ))
