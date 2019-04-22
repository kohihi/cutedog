from . import db
from datetime import datetime


class Comment(db.EmbeddedDocument):
    content = db.StringField(max_length=512)
    author = db.StringField()


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
    ok_list = db.ListField(db.StringField())
    no_list = db.ListField(db.StringField())
    ok = db.IntField(default=0)
    no = db.IntField(default=0)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    visible = db.BooleanField()
    ct = db.DateTimeField(default=datetime.now)
