from app import db
from datetime import datetime


class Comment(db.EmbeddedDocument):
    content = db.StringField(max_length=512)
    author = db.StringField()
    ct = db.DateTimeField(default=datetime.now)

    def api_data(self):
        return dict(
            content=self.content,
            author=self.author,
            ct=self.ct.__str__(),
        )


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
    w_list = db.ListField(db.StringField())
    m_list = db.ListField(db.StringField())
    w = db.IntField(default=0)
    m = db.IntField(default=0)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    visible = db.BooleanField()
    ct = db.DateTimeField(default=datetime.now)

    def api_data(self):
        return dict(
            img_id=self.img_id,
            url=self.url,
            author=self.author,
            w=self.w,
            m=self.m,
            ct=self.ct.__str__(),
            comments_num=len(self.comments),
        )
