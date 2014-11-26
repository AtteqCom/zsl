# Now import the application and the remaining stuff.
def load_peformers():
    '''
    Import in this form is necessary so that we avoid the unwanted behavior and immediate initialization of the 
    application objects. This makes the initialization procedure run in the time when it is necessary and has every 
    required resources.
    '''
    __import__('asl.interface.webservice.performers.default')
    __import__('asl.interface.webservice.performers.resource')
    __import__('asl.interface.webservice.performers.task')
    __import__('asl.interface.webservice.performers.method')

def load():
    load_peformers()
