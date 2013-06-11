import hashlib

from django.db import models

from south.modelsinspector import add_introspection_rules


_hashit = lambda s: hashlib.sha1(s).hexdigest()


class HashField(models.CharField):
    description = ('HashField is related to some other field in a model and'
        'stores its hashed value for better indexing performance.')

    def __init__(self, original, *args, **kwargs):
        '''
        :param original: name of the field storing the value to be hashed
        '''
        self.original = original
        kwargs['max_length'] = 40
        kwargs['null'] = False
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('editable', False)
        super(HashField, self).__init__(*args, **kwargs)

    def calculate_hash(self, model_instance):
        original_value = getattr(model_instance, self.original)
        setattr(model_instance, self.attname, _hashit(original_value))

    def pre_save(self, model_instance, add):
        self.calculate_hash(model_instance)
        return super(HashField, self).pre_save(model_instance, add)


# This tells South, how to store the field.
# more information: http://south.readthedocs.org/en/0.7.6/customfields.html
add_introspection_rules([
    (
        [HashField],
        [],
        {
            "original": ["original", {}],
        },
    ),
],
["^myproject\.fields\.HashField"])  # use your own path to HashField


class HashMixin(object):
    '''Model mixin for easy work with HashFields.'''

    def calculate_hashes(self):
        '''Calculate hashes of all the HashFields in the model.
        '''
        hashed_fields = [field for field in self._meta.fields
                         if isinstance(field, HashField)]
        for field in hashed_fields:
            field.calculate_hash(self)

    @classmethod
    def calculate_hash(cls, value):
        '''Calculate hash of the given value, which belongs to no specific
        field.
        '''
        return _hashit(value)
