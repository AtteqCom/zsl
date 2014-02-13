from asl.application.service_application import service_application
from asl.router import router
from flask import request
from flask.helpers import make_response
from asl.task.job_context import JobContext, WebJobContext
import traceback

app = service_application
conf = service_application.config

class WebTaskTester:
    def performTask(self, path):
        try:
            app.logger.debug("Performing task %s.", path)
            
            response = None
            if request.method == 'OPTIONS':
                response = app.make_default_options_response()
            else:
                (task, task_callable) = router.route(path)
    
                data = request.form.to_dict(flat=True)
                if request.headers.has_key("Content-Type") and request.headers["Content-Type"] == "application/json":
                    data = request.json
    
                app.logger.debug("Data found '%s'.", str(data))
                jc = WebJobContext(path, data, task, task_callable, request)
                JobContext.set_current_context(jc)
                response = make_response(task_callable(jc.task_data))
                jc.notify_responders(response)
            response.headers['ASL-Flask-Layer'] = '1.00aa0'
            response.headers['Cache-Control'] = 'no-cache'
            
            if conf.get('ALLOW_ORIGIN'):
                response.headers['Access-Control-Allow-Origin'] = conf.get('ALLOW_ORIGIN')
            response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'accept, origin, content-type'
            
            return response
        except Exception as e:
            app.logger.error(unicode(e) + "\n" + traceback.format_exc())
            raise

@app.route("/task/<path:path>", methods=["POST", "GET", "OPTIONS"])
def perform_web_task(path):
    return WebTaskTester().performTask(path)
