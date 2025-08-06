import logging
from typing import Optional, List

from tortoise.exceptions import DoesNotExist
from entity.database.mysql import User
from entity.schema.user_schema import UserOut

logger = logging.getLogger(__name__)


async def create_user_info(username: str, email: str) -> UserOut:
    """
    创建新用户
    :param username: 用户名
    :param email: 邮箱地址
    :return: Pydantic 用户对象
    """
    user = await User.create(username=username, email=email)
    logger.info(f"创建用户成功: {user.username} ({user.id})")
    return UserOut.from_orm(user)


async def get_user_by_id(user_id: int) -> Optional[UserOut]:
    """
    根据用户 ID 获取用户信息
    :param user_id: 用户 ID
    :return: Pydantic 用户对象或 None
    """
    try:
        user = await User.get(id=user_id)
        logger.debug(f"获取用户成功: ID={user_id}")
        return UserOut.from_orm(user)
    except DoesNotExist:
        logger.warning(f"用户不存在: ID={user_id}")
        return None


async def get_user_list() -> List[UserOut]:
    """
    获取所有用户列表
    :return: Pydantic 用户对象列表
    """
    users = await User.all()
    logger.info(f"获取用户列表，共 {len(users)} 个用户")
    return [UserOut.from_orm(user) for user in users]


async def update_user_info(user_id: int, **kwargs) -> Optional[UserOut]:
    """
    更新用户信息
    :param user_id: 用户 ID
    :param kwargs: 要更新的字段和值
    :return: 更新后的 Pydantic 用户对象或 None
    """
    user = await User.get_or_none(id=user_id)
    if user:
        for field, value in kwargs.items():
            if value is not None:
                setattr(user, field, value)
                logger.debug(f"更新字段: {field} -> {value}")
        await user.save()
        logger.info(f"用户更新成功: ID={user_id}")
        return UserOut.from_orm(user)
    logger.warning(f"更新失败，用户不存在: ID={user_id}")
    return None


async def delete_user_by_id(user_id: int) -> bool:
    """
    删除用户
    :param user_id: 用户 ID
    :return: 是否删除成功
    """
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        logger.info(f"用户删除成功: ID={user_id}")
        return True
    logger.warning(f"删除失败，用户不存在: ID={user_id}")
    return False
