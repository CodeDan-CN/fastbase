from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from entity.database.user import User
from exception.custom_exception import CustomErrorThrowException


async def get_user_info_by_id(id: int, session: AsyncSession):
    result = await session.exec(select(User).where(User.id == id))
    user = result.one_or_none()
    if not user:
        raise CustomErrorThrowException(status_code=404, detail="员工不存在")
    return user