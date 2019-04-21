from flask import (
    request,
    Blueprint,
)
import json
from model.count import Count
from model.wang import Wang

main = Blueprint('api', __name__)


@main.route('/image', methods=["POST"])
def post():
    data = request.get_json()
    m_data = dict()
    author = data.get('author')
    if author in ["", None]:
        author = 'Anonymous'
    m_data['author'] = author
    m_data['img_id'] = Count.get_number(Wang)
    m_data['board'] = data.get('board', 3)
    m_data['url'] = data.get('url').split(";")
    m_data['visible'] = False
    wang = Wang.new(m_data)
    wang.save()
    r = dict(
        code=0
    )
    return json.dumps(r)
