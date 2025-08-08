from fastapi import APIRouter
from core.login_core import login_handler
from entity.schema.request_schema import LoginRequest
from utils.base_response import BaseResponse

login = APIRouter()

@login.post("/login")
async def user_login(login_req: LoginRequest):
    """
    用户登录接口

    接收用户登录请求，验证用户名和密码，
    认证成功后返回包含 access_token 和 refresh_token 的登录结果。

    参数:
        login_req (LoginRequest): 请求体，包含用户名和密码

    返回:
        BaseResponse: 标准响应结构，code=200 表示成功，data 中包含 token 信息
    """
    username = login_req.username
    password = login_req.password
    result = await login_handler(username, password)
    return BaseResponse(code=200, msg="登录成功", data=result)


