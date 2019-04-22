from . import db
from datetime import datetime


class Comment(db.EmbeddedDocument):
    content = db.StringField()
    name = db.StringField(max_length=120)


class Image(db.Document):
    meta = {
        'collection': 'image',
        'ordering': ['-img_id'],
        'strict': False,
    }
    img_id = db.IntField()
    url = db.ListField(db.StringField())
    author = db.StringField()
    board = db.StringField()
    ok = db.IntField()
    no = db.IntField()
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    visible = db.BooleanField()
    ct = db.DateTimeField(default=datetime.now)
