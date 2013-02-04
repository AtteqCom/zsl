'''
Created on 31.1.2013

@author: Martin Babka
'''
from application.service_application import SportkyFlask
from injector import inject
from sportky.service.image_service import ImageService
from db.helpers.query_filter import FILTER_VALUES, FILTER_HINT, OperatorLike
from task.task_decorator import json_input, json_output

class FetchImageListTask(object):
    '''
    Fetches the image list.
    '''

    @inject(image_service=ImageService, app=SportkyFlask)
    def __init__(self, image_service, app):
        '''
        Constructor
        '''

        self._app = app
        self._image_service = image_service

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()

        self._app.logger.debug("Having data {0}.".format(data))

        f = {
            FILTER_VALUES: d['filter'],
            FILTER_HINT: {
                 'description': OperatorLike,
            }
        }

        (images, qh) = self._image_service.fetch_list(f, d['pagination'])
        app_images = []
        for image in images:
            im = image.get_app_model()
            im.url = image.get_url(d['dimension'])
            app_images.append(im)

        return {'images': app_images, 'count': qh.get_pagination().get_record_count()}
