# 定义统一返回体代码
from typing import Any
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """ 统一返回体 """
    code: int = Field(200, description="API status code")
    msg: str = Field("success", description="API status message")
    data: Any = Field(None, description="API data")
