from flask import Flask
from routes.index import main as route_index
from routes.api import main as route_api

app = Flask(__name__)
app.secret_key = "^&*jh_jhf_d_kas("


app.register_blueprint(route_index)
app.register_blueprint(route_api, url_prefix='/api')

app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'


if __name__ == "__main__":
    app.run(
        port=9001,
        host="127.0.0.1",
        debug=True,
    )
