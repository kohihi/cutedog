from flask import Flask
from flask_admin import Admin


def create_app():
    r = Flask(__name__)
    r.secret_key = "^&*jh_jhf_d_kas("

    r.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    r.config['MONGODB_SETTINGS'] = {
        'db': 'Wang',
        'host': '127.0.0.1',
        'port': 27017
    }

    r.jinja_env.variable_start_string = '{{ '
    r.jinja_env.variable_end_string = ' }}'

    return r


app = create_app()

admin = Admin(app, name='microblog', template_mode='bootstrap3')
