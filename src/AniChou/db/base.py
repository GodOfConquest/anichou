# -*- coding: utf-8 -*-

from AniChou.db.fields import from_type, Field
from AniChou.db.manager import Manager, AlreadyExists
from AniChou.utils import classproperty


class ModelBase(type):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        # Add manager to the class.
        new_class.add_to_class('objects', Manager)
        # Add fields from schema.
        schema = attrs.pop('_schema')
        if schema:
            for key, value in schema.items():
                new_class.add_to_class(key, from_type(value)())
            new_class.add_to_class('_schema', schema)
        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)
        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Model(object):
    __metaclass__ = ModelBase

    _pk = None
    _unique = []
    _schema = None
    fields = {}     # Fields as {name: filed}
    _updated_fields = () # Fields for non-standard update.
                         # Model must have function X_update for each

    @property
    def unique_fields(self):
        fields = {}
        for name in self._unique:
            fields[name] = getattr(self, name)
        return fields

    def __init__(self, **kwargs):
        self._fields_dict = {}
        self._changed = False
        self._inlist = False
        self.update(kwargs)

    def __get_pk(self):
        if not self._pk:
            self._pk = 0
            for item in self.objects.all():
                if item is self:
                    continue
                if self._pk <= item._pk:
                    self._pk = item._pk + 1
        return self._pk
    pk = property(__get_pk)

    def update(self, updates):
        updated_fileds = {}
        for key in self._updated_fields:
            try:
                updated_fileds[key] = updates.pop(key)
            except:
                pass

        for key, value in updates.iteritems():
            if not hasattr(self, key):
                raise AttributeError('Cannot change this property')
            setattr(self, key, value)

        for key, data in updated_fileds.items():
            getattr(self, '{0}_update'.format(key))(data)


    def save(self):
        self._changed = False
        try:
            self.objects.add(self)
        except AlreadyExists:
            pass
        self._inlist = True

    def delete(self):
        self.objects.delete(self)
        self._inlist = False

