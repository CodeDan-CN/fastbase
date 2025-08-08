from typing import Union

from fastapi import HTTPException

from exception.error_codes import ErrorCode


class BaseAPIException(HTTPException):
    status_code = 400
    detail = "api error"

    def __init__(self, detail: str = None, status_code: int = None):
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code


class CustomErrorThrowException(BaseAPIException):
    """
    自定义业务异常，可传入 ErrorCode 枚举或自定义 message。
    """
    def __init__(self, error: Union[ErrorCode, str], status_code: int = None):
        if isinstance(error, ErrorCode):
            detail = error.message
            status_code = status_code or error.code
        else:
            detail = str(error)
            status_code = status_code or 400

        super().__init__(detail=detail, status_code=status_code)
