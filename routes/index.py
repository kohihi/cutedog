from flask import (
    Blueprint,
    request,
    render_template
)
from model.image import Image


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
        ms = Image.objects(visible=True,).exclude('ok_list', 'no_list').paginate(page=page, per_page=20).items
    else:
        ms = None
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
        ms = Image.objects(board='dog', visible=True).paginate(page=page, per_page=20).items
    else:
        ms = None
    return render_template('index.html', ms=ms)


@main.route('/cat')
def cat():
    # key = data.get("key")
    # 这个 key 是什么东西？
    key = True
    # 验证密钥
    if key is True:
        page = 1
        if request.args.get('page') is None:
            pass
        else:
            page = int(request.args.get("page"))
        # ms = Wang.find_paginate(page=page, pre=20)
        ms = Image.objects(board='cat', visible=True).paginate(page=page, per_page=20).items
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
        ms = Image.objects(board='other', visible=True).paginate(page=page, per_page=20).items
    else:
        ms = None
    return render_template('index.html', ms=ms)
