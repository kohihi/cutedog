from app import create_app
from os import getenv
from flask_cors import CORS

app = create_app(getenv("ENV_KOHI", "dev"))
CORS(app)

if __name__ == "__main__":
    app.run(
        port=9001
    )
