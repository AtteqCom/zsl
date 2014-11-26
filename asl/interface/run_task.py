import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'));

from asl.interface import importer
importer.append_pythonpath()

from asl.application.service_application import service_application
from asl.task.job_context import JobContext
from asl.router import task_router

app = service_application
app.initialize_dependencies()

class Job():
    def __init__(self, data):
        self.data = {'data': data}

def run_task():
    if len(sys.argv) == 1:
        print "Please provide the task arguments."
        sys.exit(1)

    task = sys.argv[1]
    data = sys.argv[2] if len(sys.argv) > 2 else None

    # Open the data from file, if necessary.
    if data is not None and data.startswith("file://"):
        with open(data[len("file://"):]) as f:
            data = f.read()

    # Prepare the task.
    job = Job(data)
    (task, task_callable) = task_router.route(task)
    jc = JobContext(job, task, task_callable)
    JobContext.set_current_context(jc)

    # Run the task.
    return jc.task_callable(jc.task_data)

# Run it!
if __name__ == "__main__":
    print run_task()
