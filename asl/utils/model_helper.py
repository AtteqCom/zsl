from asl.application import service_application

def update_model(raw_model, app_model, forbidden_keys = [], inverse = False):
    '''
    Updates the `raw_model` according to the values in the `app_model`.

    @param raw_model: Raw model which gets updated.
    @param app_model: App model holding the data.
    @param forbidden_keys: Data/attributes which will not be updated.
    @param inverse: If the value is `True` all `app_model` attributes which are contained in the `raw_model` are
                    updated. If the value is `False` all `raw_model` properties which are in the `app_model` will be
                    updated.
    '''
    app = service_application

    if type(app_model) != dict:
        app_model = app_model.__dict__

    if inverse:
        for k in app_model.keys():
            app.logger.debug(u"Considering property {0}.".format(k))
            if (hasattr(raw_model, k)) and (not k in forbidden_keys):
                app.logger.debug(u"Setting property {0} to value '{1}'.".format(k, app_model[k]))
                setattr(raw_model, k, app_model[k])
    else:
        for k in raw_model.__dict__.keys():
            app.logger.debug(u"Considering property {0}.".format(k))
            if (k in app_model) and (not k in forbidden_keys):
                app.logger.debug(u"Setting property {0} to value '{1}'.".format(k, app_model[k]))
                setattr(raw_model, k, app_model[k])
