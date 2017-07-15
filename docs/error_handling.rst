Error handling
##############

Custom error handlers may be added using the following code.::

        class ForbiddenExceptionErrorHandler(ErrorHandler):
            def can_handle(self, e):
                return isinstance(e, ForbiddenException)

            def handle(self, e):
                return "Forbidden!"


        class FileNotFoundExceptionErrorHandler(ErrorHandler):
            def can_handle(self, e):
                return isinstance(e, FileNotFoundException)

            def handle(self, e):
                return "FileResource not found!"


        class DefaultErrorHandler(ErrorHandler):
            def can_handle(self, e):
                return isinstance(e, Exception)

            def handle(self, e):
                @crossdomain()
                def error_handler():
                    return "error"

                return error_handler()


        class ErrorHandlerModule(Module):
            def configure(self, binder: Binder) -> None:
                register(FileNotFoundExceptionErrorHandler())
                register(ForbiddenExceptionErrorHandler())
                register(DefaultErrorHandler())


The call to register function is best timed when a module is created. To set status code for a web response use
:class:`zsl.task.job_context.StatusCodeResponder`.
