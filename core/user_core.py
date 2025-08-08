import logging
import traceback
import uuid
from datetime import datetime
from tortoise.exceptions import IntegrityError
from core.login_core import encrypt_md5
from entity.database.mysql import User
from entity.schema.request_schema import UserCreate
from exception.custom_exception import CustomErrorThrowException
from exception.error_codes import ErrorCode


async def add_user_to_database(data: UserCreate):
    """执行用户插入，需先调用校验函数"""

    await validate_user_create(data)  # 先校验
    user_id = str(uuid.uuid4())
    now = datetime.now()
    try:
        # 新增数据到数据库表中
        await User.create(user_id=user_id,name=data.name,username=data.username,password=encrypt_md5(data.password),
            department=data.department,position=data.position,role_id=data.role_id,status=1,create_time=now,
            create_by="root",update_by="root",rank=data.rank,expired_date=data.expired_date
        )

    except IntegrityError as e:
        raise CustomErrorThrowException(ErrorCode.DB_UNIQUE_CONFLICT)

    except Exception as e:
        raise CustomErrorThrowException(ErrorCode.USER_CREATE_FAILED)

    logging.info(f"用户添加成功: {data.username}")
    return data.username

async def validate_user_create(data: UserCreate):
    """校验用户创建数据，抛出异常则校验失败"""

    if data.rank is not None and len(str(data.rank)) > 6:
        logging.error("排序字段输入长度超出限制")
        raise CustomErrorThrowException(ErrorCode.FIELD_RANK_TOO_LONG)

    if len(data.name) > 20:
        logging.error("姓名字段输入长度超出限制")
        raise CustomErrorThrowException(ErrorCode.FIELD_NAME_TOO_LONG)

    if len(data.username) > 20:
        logging.error("用户名字段输入长度超出限制")
        raise CustomErrorThrowException(ErrorCode.FIELD_USERNAME_TOO_LONG)

    username_count = await User.filter(username=data.username, status=1).count()
    if username_count > 0:
        logging.error("用户名重复，请检查")
        raise CustomErrorThrowException(ErrorCode.USERNAME_DUPLICATE)


