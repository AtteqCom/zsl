"""
:mod:`zsl.task.job_context`
---------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""

from __future__ import annotations

from abc import abstractmethod
import contextlib
from threading import current_thread
from typing import Any, Callable, Generator, TypedDict

from flask.wrappers import Request, Response

from zsl.task.task_data import TaskData
from zsl.utils.reflection_helper import proxy_object_to_delegate


class JobData(TypedDict):
    """
    A dictionary that represents the data associated with a job.

    :ivar path: The path to the job data.
    :vartype path: str
    :ivar data: The data associated with the job.
    :vartype data: dict[str, Any]

    Example:
    --------
    >>> job_data = JobData(path='/path/to/job', data={'name': 'John', 'age': 30})
    """

    path: str
    data: dict[str, Any]


class Job:
    def __init__(self, data: JobData):
        self.data = data

    @property
    def path(self) -> str:
        """Job's path.

        :getter: Returns job's path
        :type: str
        """
        return self.data["path"]

    @property
    def payload(self) -> dict[str, Any]:
        """Data part of job.

        :getter: Returns job's payload
        :type: dict
        """
        return self.data["data"]

    @property
    def is_valid(self) -> bool:
        """Validity of job's data.

        :getter: Returns if job's data are valid
        :type: bool
        """
        return self.data and "path" in self.data and "data" in self.data


class JobContext:
    """Job Context"""

    def __init__(
        self,
        job: Job,
        task: object,
        task_callable: Callable,
        *,
        task_use_master_node: bool = True,
    ):
        """
        Constructor
        """
        self._job = job
        self._task = task
        self._task_callable = task_callable
        self._task_data = TaskData(self.job.payload)
        self._task_use_master_node = task_use_master_node

        JobContext._set_current_context(self)

    @property
    def job(self) -> Job:
        return self._job

    @property
    def task(self) -> object:
        return self._task

    @property
    def task_callable(self) -> Callable:
        return self._task_callable

    @property
    def task_data(self) -> TaskData:
        return self._task_data

    @property
    def task_use_master_node(self) -> bool:
        return self._task_use_master_node

    @classmethod
    def get_current_context(cls) -> JobContext:
        return current_thread()._current_job_context

    @classmethod
    def _set_current_context(cls, context: JobContext):
        current_thread()._current_job_context = context


class Responder:
    @abstractmethod
    def respond(self, r: Response) -> None:
        pass


class StatusCodeResponder(Responder):
    def __init__(self, status_code: int):
        self._status_code = status_code

    def respond(self, r: Response) -> None:
        r.status_code = self._status_code


def add_responder(responder: Responder) -> None:
    jc = JobContext.get_current_context()
    if isinstance(jc, WebJobContext):
        jc.add_responder(responder)


class HeadersDict(TypedDict):
    Location: str


class ResponseDict(TypedDict):
    headers: HeadersDict
    status_code: int


def web_task_redirect(location) -> HeadersDict:
    return {"headers": {"Location": location}, "status_code": 301}


def create_job(path: str, data: dict[str, Any]) -> Job:
    return Job({"data": data, "path": path})


class WebJobContext(JobContext):
    def __init__(
        self,
        path: str,
        data: dict,
        task: object,
        task_callable: Callable,
        request: Request,
    ):
        """Constructor"""
        super().__init__(
            create_job(path, data), task, task_callable, task_use_master_node=False
        )
        self._request = request
        self._responders: list[Responder] = []

    def get_web_request(self) -> Request:
        return self._request

    def add_responder(self, r: Responder):
        self._responders.append(r)

    def notify_responders(self, response: Response):
        try:
            for r in self._responders:
                r.respond(response)
        finally:
            self._responders = []


class DelegatingJobContext(JobContext):
    def __init__(self, job: Job, task: object, task_callable: Callable):
        wrapped_job_context = JobContext.get_current_context()
        super().__init__(job, task, task_callable)
        self._wrapped_job_context = wrapped_job_context
        proxy_object_to_delegate(self, wrapped_job_context)

    def stop_delegating(self):
        JobContext._set_current_context(self._wrapped_job_context)


@contextlib.contextmanager
def delegating_job_context(
    job: Job, task: object, task_callable: Callable
) -> Generator[DelegatingJobContext, None, None]:
    djc = DelegatingJobContext(job, task, task_callable)
    yield djc
    djc.stop_delegating()
