import types

def app_model(model):
    '''
    Skratka pre model.get_app_model()
    '''
    
    return model.get_app_model()

# TODO mozno dat niekam inam, ako tuto skryte
def app_models(raw_models):
    '''
    Pre zoznam raw modelov vrati pole app modelov
    '''
    return [model.get_app_model() for model in raw_models]

def app_model_or_none(raw_model):
    return raw_model.get_app_model() if raw_model is not None else None

def visit_app_model(model, visitor):
    original_get_app_model = model.get_app_model
    
    def wrap(self):
        app_model = original_get_app_model()
        visitor(app_model, model)
        
        return app_model
    
    model.get_app_model = types.MethodType(wrap, model)
    
    return model