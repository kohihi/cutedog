from app import db


class Count(db.Document):
    model = db.StringField()
    count = db.IntField()

    @classmethod
    def get_number(cls, model):
        model_name = model.__name__.lower()
        count = Count.objects(model=model_name).first()
        if not count:
            count = Count(
                model=model_name,
                count=10000,
            )
            count.save()
            return count.count
        else:
            number = count.count + 1
            count.update(count=number)
            return number
