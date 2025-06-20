from fastapi import APIRouter
from core.user_core import create_user_info, get_user_by_id, get_user_list, update_user_info, delete_user_by_id
from entity.schema.user_schema import UserOut, UserCreate, UserUpdate
from exception.custom_exception import CustomErrorThrowException
from utils.base_response import BaseResponse
user = APIRouter()


@user.post("/add")
async def create_user(user: UserCreate):
    user_obj = await create_user_info(user.username, user.email)
    return BaseResponse(code=200, msg="success", data=user_obj)


@user.get("/info/{user_id}")
async def get_user(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise CustomErrorThrowException(status_code=404, detail="User not found")
    return BaseResponse(code=200, msg="success", data=user)


@user.get("/all")
async def list_users():
    return BaseResponse(code=200, msg="success", data=await get_user_list())


@user.put("/update/{user_id}")
async def update_user(user_id: int, update: UserUpdate):
    user = await update_user_info(user_id, **update.dict())
    if not user:
        raise CustomErrorThrowException(status_code=404, detail="User not found")
    return BaseResponse(code=200, msg="success", data=user)


@user.delete("/del/{user_id}")
async def delete_user(user_id: int):
    success = await delete_user_by_id(user_id)
    if not success:
        raise CustomErrorThrowException(status_code=404, detail="User not found")
    return BaseResponse(code=200, msg="User deleted", data=None)
