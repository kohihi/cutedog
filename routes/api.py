from flask import (
    request,
    Blueprint,
    session,
)
import json
from model.count import Count
from model.image import (
    Image,
    Comment,
)

main = Blueprint('api', __name__)


@main.route('/image', methods=['POST'])
def post_image():
    data = request.get_json()
    author = data.get('author')
    if author in ["", None]:
        author = 'Anonymous'
    image = Image(
        img_id=Count.get_number(Image),
        author=author,
        board=data.get('board', 'other'),
        word=data.get('word', ''),
        url=data.get('url').split(";"),
        visible=False,
    )
    image.save()
    r = dict(
        code=0
    )
    return json.dumps(r)


@main.route('/vote', methods=['PUT'])
def vote():
    """
    正负反馈api
    :return:
    00000-反馈成功
    10001-图片不存在
    10002-已经反馈过了
    10003-意料之外的参数类型
    """
    data = request.get_json()
    img_id = data.get('img_id')
    client_ip = request.headers.get("real_ip")
    vote_type = data.get('type')
    image = Image.objects(img_id=img_id).first()
    if not image:
        return json.dumps(dict(
            code=10001,
        ))
    if vote_type is 1:
        # 我觉得汪
        if client_ip in image.w_list:
            return json.dumps(dict(
                code=10002,
            ))
        image.update(push__w_list=client_ip, w=image.w+1)
    elif vote_type is 0:
        # 我觉得喵
        if client_ip in image.m_list:
            return json.dumps(dict(
                code=10002,
            ))
        image.update(push__m_list=client_ip, m=image.m+1)
    else:
        return json.dumps(dict(
            code=10003
        ))

    return json.dumps(dict(
        code=0
    ))


@main.route('/image/comment', methods=['POST'])
def post_comment():
    data = request.get_json()
    author = data.get('author')
    if author in ["", None]:
        author = 'Anonymous'
    img_id = data.get('img_id')
    image = Image.objects(img_id=img_id).first()
    if not image:
        return json.dumps(dict(
            code=10001,
        ))
    content = data.get('content')
    comment = Comment(
        author=author,
        content=content,
    )
    image.update(push__comments=comment)
    return json.dumps(dict(
        code=0,
        data=comment.api_data(),
    ))


@main.route('/image', methods=['GET'])
def get_image():
    query_set = dict(
        visible=True,
    )
    if request.args.get('board') in ("cat", "dog", "other"):
        query_set['board'] = request.args.get('board')

    try:
        page = int(request.args.get('page'))
    except ValueError as e:
        page = 1
    paginate = Image.objects(**query_set).exclude('w_list', 'm_list',).paginate(page=page, per_page=15)
    ms = paginate.items
    p = 0
    while paginate.has_next and p < 3:
        p += 1
        paginate = paginate.next()

    data = [m.api_data() for m in ms]
    return json.dumps(dict(
        code=0,
        data=data,
        page=page,
        next=p,
    ))


@main.route('/image/comment', methods=['GET'])
def get_comment():
    img_id = request.args.get("img_id")
    image = Image.objects(img_id=img_id).first()
    if not image:
        return json.dumps(dict(
            code=10001
        ))
    data = [c.api_data() for c in image.comments]
    return json.dumps(dict(
        code=0,
        data=data,
    ))


@main.route('/chat/enter', methods=['POST'])
def enter_chat():
    data = request.get_json()
    name = data.get('name')
    session['name'] = name
    return json.dumps(dict(
            code=0,
        ))
