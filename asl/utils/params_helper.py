'''
Modul na ulahcenie prace s parametrami 

@author Peter Morihladko
'''

class RequestException(Exception):
    pass

def required_params(data, *required_params):
    '''
    Skontroluje ci dane parametre sa nachadzaju v data parametre,
    ak nie vyhodi vynimku
    '''
    
    if not reduce(lambda still_valid, param: still_valid and param in data, required_params, True):
        raise RequestException(msg_err_missing_params(*required_params)) 

def msg_err_missing_params(*params):
    return "Missing one or more required parameters (%s)" % '|'.join(params)
