from asl.application import service_application

def update_model(raw_model, app_model, forbidden_keys = [], inverse = False):
    app = service_application

    if type(app_model) != dict:
        app_model = app_model.__dict__

    if inverse:
        for k in app_model.keys():
            app.logger.debug("Considering property {0}.".format(k))
            if (hasattr(raw_model, k)) and (not k in forbidden_keys):
                app.logger.debug("Setting property {0}.".format(k))
                setattr(raw_model, k, app_model[k])
    else:
        for k in raw_model.__dict__.keys():
            app.logger.debug("Considering property {0}.".format(k))
            if (k in app_model) and (not k in forbidden_keys):
                app.logger.debug("Setting property {0}.".format(k))
                setattr(raw_model, k, app_model[k])
