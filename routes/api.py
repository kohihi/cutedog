from flask import (
    request,
    Blueprint,
)
import json
from model.count import Count
from model.image import Image

main = Blueprint('api', __name__)


@main.route('/image', methods=["POST"])
def post():
    data = request.get_json()
    author = data.get('author')
    if author in ["", None]:
        author = 'Anonymous'
    wang = Image(
        img_id=Count.get_number(Image),
        author=author,
        board=data.get('board', 'other'),
        url=data.get('url').split(";"),
        visible=False,
    )
    wang.save()
    r = dict(
        code=0
    )
    return json.dumps(r)
