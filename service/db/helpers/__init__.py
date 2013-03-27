# TODO mozno dat niekam inam, ako tuto skryte
def app_models(raw_models):
    '''
    Pre zoznam raw modelov vrati pole app modelov
    '''
    return [model.get_app_model() for model in raw_models]
