from typing import Annotated

from fastapi import APIRouter, Depends

from core.login_core import get_current_active_user
from core.user_core import add_user_to_database
from entity.database.mysql import User
from entity.schema.request_schema import UserCreate
from utils.base_response import BaseResponse

user = APIRouter()

@user.post("/add")
async def add_user(data: UserCreate):
    """
    新增用户接口

    接收用户创建请求数据，调用数据库操作函数新增用户，
    并返回标准响应结果。

    参数:
        data (UserCreate): 用户创建请求体，包含新增用户所需字段

    返回:
        BaseResponse: 标准响应格式，code=200表示操作成功，data为空
    """
    await add_user_to_database(data)
    return BaseResponse(code=200,msg="新增成功", data=None)

@user.get("/test/{id}")
async def read_users_me(
        id:int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    print(id)
    return current_user.user_id
