from asl.client import RawTask, WebService, JsonTask, JsonTaskResult,\
    SecuredTask

#
# Usage example to express the idea of working with Atteq Service Layer.
#

# create client
web_config = {'SERVICE_LAYER_URL': 'http://my.service.layer.url/task/'}
security_config = {'SECURITY_TOKEN': 'my super secret secure token'}

web_service = WebService(web_config, security_config)


# prepare task
# task data doesn't have to be dictionary. It depends on task and TaskDecorators
# (see bellow) you use
task = RawTask('example/my_super_task', {'motto': 'hate haters', 'frequency': 'every day'})

# call task with some decorators
#
# task is decorated with given TaskDecorator's. TaskDecorator's are responsible
# for processing task data to suitable format (= format that is expected on
# service layer side). If you want to chain more TaskDecorator's together,
# simply put them in array (second parameter of WebService.call() method)
# in desirable order.
#
# we get task_result which is TaskResult instance "decorated" (in this case) with
# JsonTaskResult. TaskResultDecorator's are responsible for processing data
# we get as response to our "call task" request. If you want to chain more
# TaskDecorator's together, simply put them in array (second parameter of
# WebService.call() method) in desirable order.
#
task_result = web_service.call(task, [SecuredTask, JsonTask, JsonTaskResult])

# to get result (of request to service layer) parsed with given TaskResultDecorator's
# simply call get_result() method
result = task_result.get_result()
