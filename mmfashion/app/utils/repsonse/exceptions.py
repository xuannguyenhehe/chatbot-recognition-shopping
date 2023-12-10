from fastapi import Request
from starlette.responses import JSONResponse


class ExceptionBase(Exception):
    def __init__(self, status_code: int, message: str):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return (
            f"<Exception {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: ExceptionBase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class ExceptionResponse(object):
    class ErrorServer(ExceptionBase):
        def __init__(self, message: str = None):
            """
            Error server
            """
            status_code = 400
            message = "Error server"
            ExceptionBase.__init__(self, status_code, message)

    class WrongPassword(ExceptionBase):
        def __init__(self, message: str = None):
            """
            Wrong password
            """
            status_code = 400
            message = "Wrong password"
            ExceptionBase.__init__(self, status_code, message)

    class RePassword(ExceptionBase):
        def __init__(self, message: str = None):
            """
            Need to re-password
            """
            status_code = 400
            message = "Need to re-password"
            ExceptionBase.__init__(self, status_code, message)

    class ExistedError(ExceptionBase):
        def __init__(self, context: dict = None):
            """
            Existed error
            """
            status_code = 400
            message = ""
            if len(context) > 0:
                for key, value in context.items():
                    message += f"Existed {key} {value}"
            ExceptionBase.__init__(self, status_code, message)

    class NoExistedError(ExceptionBase):
        def __init__(self, context: dict = None):
            """
            No existed error
            """
            status_code = 400
            message = ""
            if len(context) > 0:
                for key, value in context.items():
                    message += f"No existed {key} {value}"
            ExceptionBase.__init__(self, status_code, message)
