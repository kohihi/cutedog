from flask import (
    Blueprint,
    request,
    render_template
)
from model.wang import Wang
from model.count import Count
import json

main = Blueprint('index', __name__)


@main.route('/')
def index():
    # key = data.get("key")
    key = True
    # 验证密钥
    if key is True:
        page = 1
        if request.args.get('page') is None:
            pass
        else:
            page = int(request.args.get("page"))
        # ms = Wang.find_paginate(page=page, pre=20)
        ms = Wang.find_paginate(20, page, deleted=False, visible=True)
    else:
        ms = None
    print("MS is:", ms)
    return render_template('index.html', ms=ms)


@main.route('/dog')
def dog():
    # key = data.get("key")
    key = True
    # 验证密钥
    if key is True:
        page = 1
        if request.args.get('page') is None:
            pass
        else:
            page = int(request.args.get("page"))
        # ms = Wang.find_paginate(page=page, pre=20)
        ms = Wang.find_paginate(20, page, deleted=False, board=1, visible=True)
    else:
        ms = None
    return render_template('index.html', ms=ms)


@main.route('/cat')
def cat():
    # key = data.get("key")
    key = True
    # 验证密钥
    if key is True:
        page = 1
        if request.args.get('page') is None:
            pass
        else:
            page = int(request.args.get("page"))
        # ms = Wang.find_paginate(page=page, pre=20)
        ms = Wang.find_paginate(20, page, deleted=False, board=2, visible=True)
    else:
        ms = None
    return render_template('index.html', ms=ms)


@main.route('/other')
def other():
    # key = data.get("key")
    key = True
    # 验证密钥
    if key is True:
        page = 1
        if request.args.get('page') is None:
            pass
        else:
            page = int(request.args.get("page"))
        # ms = Wang.find_paginate(page=page, pre=20)
        ms = Wang.find_paginate(20, page, deleted=False, board=3, visible=True)
    else:
        ms = None
    return render_template('index.html', ms=ms)


@main.route('/post', methods=["POST"])
def post():
    data = request.get_json()
    m_data = dict()
    m_data['author'] = data.get('author', 'Anonymous')
    m_data['img_id'] = Count.get_number(Wang)
    m_data['board'] = data.get('board', 3)
    m_data['url'] = data.get('url').split(";")
    m_data['visible'] = False
    wang = Wang.new(m_data)
    wang.save()
    return "ok"
