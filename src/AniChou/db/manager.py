
import operator
from AniChou.db.pickle import PickleDB
from AniChou.utils import classproperty

manager_cache = {}


__all__ = ['DoesNotExists', 'MultipleObjectsReturned', 'AlreadyExists',
           'Manager']


class DoesNotExists(ValueError):
    pass


class MultipleObjectsReturned(ValueError):
    pass


class AlreadyExists(ValueError):
    pass


class Manager(object):

    __db = None

    @classmethod
    def contribute_to_class(selfcls, cls, name):
        if not cls in manager_cache:
            manager_cache[cls] = Manager(cls)
        setattr(cls, name, manager_cache[cls])

    @classmethod
    def __get_db(cls, *args, **kwargs):
        if not cls.__db:
            cls.__db = PickleDB()
        return cls.__db
    db = classproperty(__get_db)

    @staticmethod
    def __filterfunc(item, key, value):
        (key, op) = key.partition('__')[::2]
        operation = getattr(operator, op or 'eq')
        return operation(getattr(item, key), value)

    def __init__(self, model):
        self.__model = model

    def __get_data(self):
        try:
            return list(self.db[self.__model])
        except KeyError:
            self.db[self.__model] = []
        return []
    data = property(__get_data)

    def all(self):
        return self.data

    def get(self, **kwargs):
        r = self.filter(**kwargs)
        if len(r) > 1:
            raise MultipleObjectsReturned
        elif not r:
            raise DoesNotExists
        return r[0]

    def get_or_create(self, **kwargs):
        created = False
        try:
            obj = self.get(**kwargs)
        except DoesNotExist:
            obj = self.__model(**kwargs)
            created = True
            self.add(obj)
        return [obj, created]

    def filter(self, **kwargs):
        ret = self.data
        for key, value in kwargs.iteritems():
            if not ret:
                break
            ret = filter(lambda x: self.__filterfunc(x, key, value), ret)
        return ret

    def add(self, obj):
        try:
            self.get(obj.unique_fields)
        except DoesNotExists:
            pass
        else:
            raise AlreadyExists
        if self.__model not in self.db.keys():
            self.db[self.__model] = []
        self.db[self.__model].append(obj)

    def save(self):
        self.db.write(self.data)

    def delete(self, item):
        if self.__model not in self.db.keys():
            raise ValueError(
            'Model {0} instance not found in database.'.format(
            type(self.__model)))
        self.db[self.__model].remove(item)
