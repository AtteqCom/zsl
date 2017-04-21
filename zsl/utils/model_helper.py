"""
:mod:`zsl.utils.model_helper`
-----------------------------

Helper module for working with models.
"""

from __future__ import unicode_literals

import logging


def update_model(raw_model, app_model, forbidden_keys=None, inverse=False):
    """Updates the `raw_model` according to the values in the `app_model`.

    :param raw_model: Raw model which gets updated.
    :param app_model: App model holding the data.
    :param forbidden_keys: Data/attributes which will not be updated.
    :type forbidden_keys: list
    :param inverse: If the value is `True` all `app_model` attributes which are contained in the `raw_model` are
                    updated. If the value is `False` all `raw_model` properties which are in the `app_model` will be
                    updated.
    """
    if forbidden_keys is None:
        forbidden_keys = []

    if type(app_model) != dict:
        app_model = app_model.__dict__

    if inverse:
        for k in app_model:
            logging.debug("Considering property {0}.".format(k))
            if (hasattr(raw_model, k)) and (k not in forbidden_keys):
                logging.debug("Setting property {0} to value '{1}'.".format(k, app_model[k]))
                setattr(raw_model, k, app_model[k])
    else:
        for k in raw_model.__dict__:
            logging.debug("Considering property {0}.".format(k))
            if (k in app_model) and (k not in forbidden_keys):
                logging.debug("Setting property {0} to value '{1}'.".format(k, app_model[k]))
                setattr(raw_model, k, app_model[k])
