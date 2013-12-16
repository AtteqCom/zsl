# TODO mozno dat niekam inam, ako tuto skryte
def app_models(raw_models):
    '''
    Pre zoznam raw modelov vrati pole app modelov
    '''
    return [model.get_app_model() for model in raw_models]

def app_model_or_none(raw_model):
    return raw_model.get_app_model() if raw_model is not None else None