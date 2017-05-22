"""
:mod:`zsl.db.helpers.nested`
----------------------------

.. moduleauthor:: peter
"""
from __future__ import unicode_literals


def nested_model(model, nested_fields):
    """
    Return app_model with nested models attached. ``nested_fields`` can
    be a simple list as model fields, or it can be a tree definition
    in dict with leafs as keys with None value
    """

    if model is None:
        return None

    app_model = model.get_app_model()
    is_dict = isinstance(nested_fields, dict)

    for field in nested_fields:
        nested_nested = nested_fields.get(field) if is_dict and nested_fields.get(field) else []
        value = getattr(model, field, None)

        # we can have also lists in field
        nm_fn = nested_models if isinstance(value, list) else nested_model

        setattr(app_model, field, nm_fn(value, nested_nested))

    return app_model


def nested_models(models, nested_fields):
    """
    For a list of ``models`` apply ``get_nested_model`` with given ``nested_fields``
    """
    return [nested_model(model, nested_fields) for model in models]
