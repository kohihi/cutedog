from model import Model


class Wang(Model):
    __fields__ = Model.__fields__ + [
        ('img_id', str, ''),
        ('url', str, ''),
        ('author', str, ''),
        ('board', str, ''),
        ('ok', int, 0),
        ('no', int, 0),
        ('comment', str, ''),
        ('visible', str, ''),
    ]
