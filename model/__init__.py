from flask_mongoengine import MongoEngine
from app import app


db = MongoEngine(app)

# client = MongoClient()
# db = client.Wang

# class Model(object):
#     """
#     所有 model 的基类
#      """
#     __fields__ = [
#         '_id',
#         ('type', str, ''),
#         ('deleted', bool, False),
#         ('ct', str, 0),
#         ('ut', str, 0),
#     ]
#
#     def __repr__(self):
#         classname = self.__class__.__name__
#         properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
#         s = '\n'.join(properties)
#         return '< {}\n{}\n>\n'.format(classname, s)
#
#     @classmethod
#     def _new_from_dict(cls, d):
#         """
#         使用 dict 生成新的 model 对象
#         :param d: class 参数字典
#         :return:
#         """
#         # 使用空字典实例化一个对象
#         m = cls()
#         fields = cls.__fields__.copy()
#         fields.remove('_id')
#         # 从 d 中将 class 属性取出
#         for f in fields:
#             # key，type，value
#             k, t, v = f
#             if k in d:
#                 setattr(m, k, d[k])
#             else:
#                 setattr(m, k, v)
#         m.type = cls.__name__.lower()
#         return m
#
#     @classmethod
#     def _new_with_db(cls, dbs):
#         """
#         给内部 all() 使用
#         从 mongo 数据中恢复一个 model
#         :param dbs: 一个 mongo 数据
#         :return: m: 一个 cls 的实例
#         """
#         m = cls()
#         fields = cls.__fields__.copy()
#         fields.remove('_id')
#         for f in fields:
#             # key，type，value
#             k, t, v = f
#             if k in dbs:
#                 setattr(m, k, dbs[k])
#             else:
#                 setattr(m, k, v)
#         setattr(m, '_id', dbs['_id'])
#         m.type = cls.__name__.lower()
#         return m
#
#     @classmethod
#     def _find(cls, **kwargs):
#         name = cls.__name__
#         flag_sort = '__sort'
#         sort = kwargs.pop(flag_sort, None)
#         ds = db[name].find(kwargs)
#         # 按照 ut 更新时间降序
#         ds.sort([("ut", -1)])
#         if sort is not None:
#             ds = ds.sort(sort)
#         l = [cls._new_with_db(d) for d in ds]
#         return l
#
#     # 使用了基类 model 的 _new_from_dict(), 尝试停用所有 Model 子类的此函数
#     # def from_form(self, form):
#     #     log('init pass')
#     #     pass
#
#     @classmethod
#     def new(cls, form, **kwargs):
#         m = cls()
#         m = m._new_from_dict(form)
#         t = format_time()
#         setattr(m, 'ct', t)
#         setattr(m, 'ut', t)
#         for k, v in kwargs.items():
#             setattr(m, k, v)
#         return m
#
#     @classmethod
#     def all(cls, **kwargs):
#         log('models, l-73 is all')
#         """
#         得到所有 models
#         :return:
#         """
#         return cls._find(**kwargs)
#
#     @classmethod
#     def find_one(cls, **kwargs):
#         l = cls._find(**kwargs)
#         if len(l) > 0:
#             return l[0]
#         else:
#             return None
#
#     @classmethod
#     def find_by(cls, **kwargs):
#         return cls.find_one(**kwargs)
#
#     @classmethod
#     def find_all(cls, **kwargs):
#         return cls._find(**kwargs)
#
#     def save(self):
#         name = self.__class__.__name__
#         db[name].save(self.__dict__)
#
#     @classmethod
#     def delete(cls, m_id):
#         name = cls.__name__
#         query = {
#             '_id': ObjectId(m_id),
#         }
#         values = {
#             'deleted': True
#         }
#         db[name].update_one(query, {"$set": values})
#
#     @classmethod
#     def find_fuzzy(cls, tag):
#         name = cls.__name__
#         ds = db[name].find({'tag': {"$regex": tag}, "deleted": False})
#         # db.posts.find({tags: {$regex: "run"}})
#         # 按照 ut 更新时间降序
#         ds.sort([("ut", -1)])
#         l = [cls._new_with_db(d) for d in ds]
#         return l
#
#     @classmethod
#     def find_paginate(cls, pre, page, **kwargs):
#         name = cls.__name__
#         count = pre * (page - 1)
#         print("limit", pre, "skip", count)
#         ds = db[name].find(kwargs).limit(pre).skip(count)
#         ds.sort([("ut", -1)])
#         l = [cls._new_with_db(d) for d in ds]
#         return l
#
#
# # 测试
# def test_find_fuzzy():
#     from models.art import Art
#     m = Art()
#     r = m.find_fuzzy(['test1', 'leetcode'])
#     print(r)
#
#
# if __name__ == '__main__':
#     test_find_fuzzy()
