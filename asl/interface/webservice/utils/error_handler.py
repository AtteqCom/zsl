'''
Created on 25.11.2014

@author: Martin Babka
'''
import traceback
from asl.application.service_application import service_application
from functools import wraps

def error_handler(f):
    '''
    Default error handler.
     - On server side error shows a message 'An error occurred!' and returns 500 status code.
     - Also serves well in the case when the resource/task/method is not found - returns 404 status code.
    '''

    @wraps(f)
    def error_handling_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ImportError as ie:
            service_application.logger.error(unicode(ie) + "\n" + traceback.format_exc())
            return unicode(ie), 404
        except Exception as e:
            service_application.logger.error(unicode(e) + "\n" + traceback.format_exc())
            return "An error occurred!", 500

    return error_handling_function
