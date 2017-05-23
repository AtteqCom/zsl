"""
:mod:`zsl.cache.id_helper`
--------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from future.utils import with_metaclass
from builtins import object
import abc
from zsl.db.model.app_model_json_decoder import get_json_decoder
from zsl.db.model.app_model_json_encoder import AppModelJSONEncoder
import json
from zsl.db.model.app_model import AppModel, RELATED_FIELDS_HINTS,\
    RELATED_FIELDS_CLASS, RELATED_FIELDS
from zsl.utils.import_helper import fetch_class


def encoder_identity(x):
    return x


def decoder_identity(module_name, x):
    return x


def app_model_decoder_fn(model_key, x):
    class_name = model_key.split(":", 1)[0]
    hints = model_key_hint_extractor(model_key)
    return json.loads(x, cls=get_json_decoder(class_name, hints)) if x is not None else None


def app_model_encoder_fn(x):
    return json.dumps(x, cls=AppModelJSONEncoder)


def create_key_class_prefix(cls):
    return "{0}.{1}".format(cls.__module__, cls.__name__)


def create_key_object_prefix(obj):
    return create_key_class_prefix(obj.__class__)


def model_key_generator(model):
    # TODO: Test
    def get_app_model_related_fields(app_model, prefix=''):
        """
        Fetches the list of related fields of the model.
         - checks for the AppModel instances.
         - checks in the lists and tuples.
        """
        d = app_model.__dict__
        related = set()
        for key in d:
            v = d[key]
            if isinstance(v, AppModel):
                related.add(prefix + key + '=' + create_key_object_prefix(v))
                related.update(get_app_model_related_fields(v, prefix + key + '__'))
            elif isinstance(v, list) or isinstance(v, tuple):
                for val in v:
                    related.add(prefix + key + '=' + create_key_object_prefix(val))
                    related.update(get_app_model_related_fields(v[0], prefix + key + '__'))

        return related

    related = sorted(get_app_model_related_fields(model))
    if len(related):
        return "{0}:{1}:+{2}".format(create_key_object_prefix(model), model.get_id(), "+".join(related))
    else:
        return "{0}:{1}".format(create_key_object_prefix(model), model.get_id())

# TODO: Test


def model_key_hint_extractor(key):
    splitted_key = key.split(':')
    if len(splitted_key) == 2:
        return None
    # The first is empty
    related = splitted_key[2].split('+')[1:]
    hints = {RELATED_FIELDS: {}}
    for r in related:
        path = r.split('=')[0].split('__')
        cls = fetch_class(r.split('=')[1])
        h = hints
        for p in path[:-1]:
            h = h[RELATED_FIELDS][p][RELATED_FIELDS_HINTS]

        rh = h[RELATED_FIELDS]
        if path[-1] not in rh:
            rh[path[-1]] = {
                RELATED_FIELDS_CLASS: cls,
                RELATED_FIELDS_HINTS: {
                    RELATED_FIELDS: {
                    }
                }
            }

    return hints


class IdHelper(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def gather_page(self, page_key, decoder=decoder_identity):
        pass

    @abc.abstractmethod
    def fill_page(self, page_key, data, timeout, encoder=encoder_identity, model_key_generator=model_key_generator):
        pass

    @abc.abstractmethod
    def check_page(self, page_key):
        pass

    @abc.abstractmethod
    def check_key(self, key):
        pass

    @abc.abstractmethod
    def get_key(self, key):
        pass

    @abc.abstractmethod
    def invalidate_key(self, key):
        pass

    @abc.abstractmethod
    def invalidate_keys_by_prefix(self, key_prefix):
        pass

    @abc.abstractmethod
    def set_key(self, key, value, timeout):
        pass
