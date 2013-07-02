import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'));

from asl.interface import importer
importer.append_pythonpath()

from asl.application.service_application import service_application
from asl.task.job_context import JobContext
from asl.router import router

app = service_application
app.initialize_dependencies()

class Job():
    def __init__(self, data):
        self.data = {'data': data}

def run_task():
    if len(sys.argv) == 1:
        print "Please provide argumets"
        sys.exit(1)  
    
    task = sys.argv[1]
    data = sys.argv[2] if len(sys.argv) > 2 else None
    
    job = Job(data)
    
    (task, task_callable) = router.route(task)
    jc = JobContext(job, task, task_callable)
    JobContext.set_current_context(jc)
    return jc.task_callable(jc.task_data)

# Run it!
if __name__ == "__main__":
    print run_task()
