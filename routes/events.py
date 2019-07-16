from flask import request
from flask import Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from urllib.parse import unquote
from app import app
from utils.chat import IDPull, Counter

socketio = SocketIO()
id_pull = IDPull(app.config['CHAT_ROOM_MAX_NUM'])
counter = Counter()


main = Blueprint('socketio', __name__)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    index = id_pull.query()
    if index is False:
        return "max"

    room = message['room']
    name = unquote(message['name'])
    join_room(room)

    sid = request.sid
    id_pull.set(index, sid)

    emit('status', {'msg': '{} #{} has entered the room'.format(name, index)}, room=room)
    update_online_num(1)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message.get('room')
    name = unquote(message.get('name'))
    leave_room(room)

    sid = request.sid
    index = id_pull.freed(sid)
    if index is None:
        data = dict(
            code=10000,
            msg='sid is None'
        )
        return_error(data, sid)
        return
    emit('status', {'msg': '{} #{} has left the room on left'.format(name, index)}, room=room)
    update_online_num(-1)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message.get('room')
    msg = unquote(message.get('msg'))
    name = unquote(message.get('name'))

    sid = request.sid
    index = id_pull.get(sid)
    if index is None:
        data = dict(
            code=10001,
            msg='Server error, please join the room again'
        )
        return_error(data, sid)
        return
    emit('message', {'msg': '{} #{}: {}'.format(name, index, msg)}, room=room)


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    sid = request.sid
    index = id_pull.freed(sid)
    if index is None:
        return
    room = "wangmiao"
    emit('status', {'msg': '#{} has left the room on disconnect'.format(index)}, room=room)
    update_online_num(-1)


@socketio.on('connect', namespace='/chat')
def connect():
    sid = request.sid
    join_room('site')
    emit('update_online', {'msg': counter.current}, room=sid)


def update_online_num(num):
    counter.plus(num)
    emit('update_online', {'msg': counter.current}, room='site')


def return_error(data, sid):
    emit('error_handler', data, room=sid)
