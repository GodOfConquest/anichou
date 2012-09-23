
from datetime import datetime

__all__ = ['from_type', 'Field', 'TypedField', 'NumberField',
           'StringField', 'DatetimeField', 'ListField', 'DictField']


def from_type(t):
    """
    Returns TypedField based on type t or returns Field if no
    such TypedField.
    """
    if not isinstance(t, type):
        raise TypeError('Only types allowed.')
    for field in (NumberField, StringField, DatetimeField,
                  ListField, DictField):
        if t in field._types:
            return field
    return Field


class Field(object):
    _value = None

    def __get__(self, caller):
        return self._value

    def __set__(self, caller, value):
        self._value = value

    def contribute_to_class(self, cls, name):
        cls.fields[name] = self
        setattr(cls, name, property(self.__get__, self.__set__))


class TypedField(Field):
    _types = (object,)
    def __set__(self, caller, value):
        if type(value) not in self._types:
            raise TypeError('Type of {0} does not match {1}'.format(
                value, self._types))
        self._value = value


class NumberField(TypedField):
    _types = (int, float, long,)


class StringField(TypedField):
    _types = (basestring, unicode,)


class DatetimeField(TypedField):
    _types = (datetime,)


class ListField(TypedField):
    _types = (list,)


class DictField(TypedField):
    _types = (dict,)
