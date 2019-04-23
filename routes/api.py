from flask import (
    request,
    Blueprint,
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
    client_ip = request.remote_addr
    vote_type = data.get('type')
    image = Image.objects(img_id=img_id).first()
    if not image:
        return json.dumps(dict(
            code=10001,
        ))
    if client_ip in image.ok_list or client_ip in image.no_list:
        return json.dumps(dict(
            code=10002,
        ))
    if vote_type is 1:
        # 我觉得ok
        image.update(push__ok_list=client_ip, ok=image.ok+1)
    elif vote_type is 0:
        # 我觉得不行
        image.update(push__no_list=client_ip, no=image.no+1)
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
    content = data.get('comment')
    comment = Comment(
        author=author,
        content=content,
    )
    image.update(push__comments=comment)
    return json.dumps(dict(
        code=0,
    ))


@main.route('/image', methods=['GET'])
def get_image():
    query_set = dict(
        visible=True,
    )
    if request.args.get('board') in ("cat", "dog", "other"):
        query_set['board'] = request.args.get('board')

    page = request.args.get('page')
    if type(page) is not int:
        page = 1
    ms = Image.objects(**query_set).exclude('ok_list', 'no_list',).paginate(page=page, per_page=20).items
    data = [m.api_data() for m in ms]
    return json.dumps(dict(
        code=0,
        data=data,
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
