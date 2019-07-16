from flask import Flask
from config import settings
from flask_mongoengine import MongoEngine
from os import getenv

db = MongoEngine()


def create_app():
    config_name = getenv("ENV_KOHI", "dev")
    a = Flask(__name__)
    a.config.from_object(settings[config_name])
    a.jinja_env.variable_start_string = '{{ '
    a.jinja_env.variable_end_string = ' }}'

    db.init_app(a)
    return a


app = create_app()
