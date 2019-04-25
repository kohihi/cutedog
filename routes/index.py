from flask import (
    Blueprint,
    render_template,
    send_file,
)


main = Blueprint('index', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/favicon.ico')
def ico():
    return send_file('favicon.ico')
