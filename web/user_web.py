from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from core.user_core import get_user_info_by_id
from utils.base_response import BaseResponse
from utils.custon_annotation import get_session

user = APIRouter()

@user.get("/info/{id}", tags=["question"], summary="通过员工ID查询员工信息")
async def get_user_info(id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_info_by_id(id, session)
    return BaseResponse(code=200, msg="success", data=user)