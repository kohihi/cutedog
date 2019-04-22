from . import db


class Count(db.Document):
    model = db.StringField()
    count = db.IntField()

    @classmethod
    def get_number(cls, model):
        model_name = model.__name__.lower()
        query_set = Count.objects(model=model_name)
        if len(query_set) is 0:
            print("count is []")
            count = Count(
                model=model_name,
                count=10000,
            )
            count.save()
            model_number = 10000
        else:
            print('count is not []')
            count = query_set[0]
            model_number = count.count + 1
            count.count = model_number
            count.save()
        return model_number
