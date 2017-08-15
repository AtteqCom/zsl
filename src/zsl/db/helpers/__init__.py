from __future__ import unicode_literals

import types


def app_model(model):
    """
    Just a convenience shortcut for `model.get_app_model()`
    """

    return model.get_app_model()


# TODO: This is quite hidden, and we could replace the function to a more convenient location.
def app_models(raw_models):
    """
    For a list of raw models return the list of the corresponding app models.
    """
    return [model.get_app_model() if model is not None else None for model in raw_models]


def app_model_or_none(raw_model):
    """
    Transforms `raw_model` to its application model. Function can handle `None` value.
    """
    return raw_model.get_app_model() if raw_model is not None else None


def visit_app_model(model, visitor):
    original_get_app_model = model.get_app_model

    def wrap(self):
        app_model = original_get_app_model()
        visitor(app_model, model)

        return app_model

    model.get_app_model = types.MethodType(wrap, model)

    return model
