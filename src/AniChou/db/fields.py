# -*- coding: utf-8 -*-

import datetime

__all__ = ['from_type', 'Field', 'TypedField', 'NumberField',
           'StringField', 'DatetimeField', 'ListField', 'DictField']

DATE_INPUT_FORMATS = (
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',
    '%b %d %Y', '%b %d, %Y',
    '%d %b %Y', '%d %b, %Y',
    '%B %d %Y', '%B %d, %Y',
    '%d %B %Y', '%d %B, %Y',
)

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
    def __get__(self, caller):
        return getattr(caller, '_fields_dict', {}).get(self.name)

    def __set__(self, caller, value):
        caller._changed = datetime.datetime.now()
        if not hasattr(caller, '_fields_dict'):
            caller._fields_dict = {}
        caller._fields_dict[self.name] = self.to_python(value)

    def to_python(self, value):
        return value

    def contribute_to_class(self, cls, name):
        self.name = name
        cls.fields[name] = self
        setattr(cls, name, property(self.__get__, self.__set__))


class TypedField(Field):
    ERRORS = {
        'bad_type': 'Bad input type',
        'undefined_types': 'Types for field not defined'
    }

    def to_python(self, value):
        try:
            return self._types[-1](value)
        except IndexError:
            raise ValueError(self.ERRORS['undefined_types'])
        except Exception as e:
            raise TypeError(self.ERRORS['bad_type'] + unicode(e))


class NumberField(TypedField):
    _types = (int, float, long,)


class StringField(TypedField):
    _types = (basestring, unicode,)


class DatetimeField(TypedField):
    _types = (datetime.datetime,)
    input_formats = DATE_INPUT_FORMATS

    def to_python(self, value):
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        for format in self.input_formats:
            try:
                return self.strptime(value, format)
            except (ValueError, TypeError):
                continue
        raise ValueError(self.ERRORS['bad_type'])

    def strptime(self, value, format):
        return datetime.datetime.strptime(value, format)


class ListField(TypedField):
    _types = (list,)


class DictField(TypedField):
    _types = (dict,)

