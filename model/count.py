from . import Model


class Count(Model):
    __fields__ = Model.__fields__ + [
        ('model', str, ''),
        ('count', str, ''),
    ]

    @classmethod
    def get_number(cls, model):
        model_name = model.__name__.lower()
        count = Count.find_by(model=model_name)
        if count is None:
            count = Count.new(
                {
                    'model': model_name,
                    'count': 10000,
                }
            )
            count.save()
            model_number = 10000
        else:
            model_number = int(count.count) + 1
            count.count = model_number
            count.save()
        return model_number
