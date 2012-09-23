
from AniChou.db.fields import from_type
from AniChou.db.manager import Manager
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
        # Add fields from scheme.
        scheme = attrs.pop('_scheme')
        if scheme:
            for key, value in scheme.items():
                new_class.add_to_class(key, from_type(value)())
            new_class.add_to_class('_scheme', scheme)
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

    _unique = []
    _scheme = None
    fields = {}

    @property
    def unique_fields(self):
        fields = {}
        for name in self._unique:
            fields[name] = getattr(self, name)
        return fields

    def __init__(self, **kwargs):
        for key, value in kwargs:
            field = getattr(self, key)
            if not isinstance(Field, field):
                raise TypeError(
                    'Cannot overwrite non-field property {0}.'.format(key))
            field.set(value)

    def save(self):
        self.objects.add(self)

    def delete(self):
        self.objects.delete(self)



