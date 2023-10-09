from loguru import logger
import inspect
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.repsonse.exceptions import ExceptionBase


class ResultResponse(object):
    def __init__(self, arg):
        if isinstance(arg, ExceptionBase):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
            self.message = arg.message
            self.value = None
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
            self.value = None
            if len(arg) >= 2:
                self.message = arg[0]
                self.status_code = arg[1]
            if len(arg) == 3:
                self.value = arg[2]

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ResultResponse Success>"
        return f"<ResultResponse Exception {self.exception_case}>"

    def __enter__(self):
        content = {}
        if hasattr(self, "message") and self.message:
            content.update({"message": self.message})
        if self.value:
            content.update({"data": self.value})
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder(content)
        )

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ResultResponse):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            return exception
    with result as result:
        return result
