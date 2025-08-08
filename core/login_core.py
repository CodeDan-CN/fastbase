import traceback
import logging
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from config.setting import settings
from entity.database.mysql import User
from entity.schema.response_schema import LoginResponse
from exception.custom_exception import CustomErrorThrowException
from exception.error_codes import ErrorCode
from hashlib import md5

SECRET_KEY = settings.jwt["secret_key"]
ALGORITHM = settings.jwt["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt["access_token_expire_minutes"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def login_handler(username: str, password: str) -> LoginResponse:
    """
    用户登录处理函数

    1. 验证用户名和密码是否为空，不满足则抛出异常；
    2. 对密码进行 MD5 加密处理；
    3. 查询数据库，验证用户存在且状态正常；
    4. 用户验证通过后，生成 JWT 访问令牌(access_token)；
    5. 返回封装好的登录响应(LoginResponse)，包含用户名和访问令牌。

    参数:
        username (str): 用户名
        password (str): 用户密码

    返回:
        LoginResponse: 包含用户名、访问令牌和刷新令牌（目前刷新令牌为空字符串）
    """
    if not username or not password:
        logging.error("[login] username or password is empty")
        raise CustomErrorThrowException(ErrorCode.USERNAME_OR_PASSWORD_UNDEFINED)
    # 进行加密过程
    password = encrypt_md5(password)
    # 查询数据库确定是否存在此人
    user = await User.get_or_none(username=username, password=password, status=1)
    if not user:
        logging.error(f"[login] username：{username}的账号不存在")
        raise CustomErrorThrowException(ErrorCode.USER_NOT_FOUND)
    expired_date = user.expired_date
    if expired_date and expired_date < datetime.now(timezone.utc):
        logging.error("用户已过期，请联系管理员！")
        raise CustomErrorThrowException(ErrorCode.USER_ACCOUNT_EXPIRED)
    # 存在开始创建token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    logging.info(f"[Login] 用户{username}登录系统，账号有效期至：{expired_date or '无期限'}")
    user.last_login_time = datetime.now(timezone.utc)
    await user.save()
    return LoginResponse(username=user.username, access_token=access_token,refresh_token="")

async def get_user(username: str):
    """
    根据用户名从数据库异步获取对应的用户对象。

    参数:
        username (str): 用户名

    返回:
        User对象或None: 如果数据库中存在对应用户名的用户，则返回User对象，否则返回None。
    """
    return await User.get_or_none(username=username)


def encrypt_md5(password):
    """
    对传入的明文密码进行MD5加密，并返回加密后的十六进制字符串。

    参数:
        password (str): 明文密码字符串

    返回:
        str: MD5加密后的十六进制摘要字符串
    """
    new_md5 = md5()
    new_md5.update(password.encode(encoding='utf-8'))
    return new_md5.hexdigest()


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    创建JWT访问令牌，默认过期时间为15分钟，可自定义过期时长。

    参数:
        data (dict): 需要存入token payload的数据，通常包含用户身份信息
        expires_delta (timedelta, optional): 令牌的过期时间差，默认为None，表示15分钟

    返回:
        str: 编码后的JWT字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    FastAPI依赖函数，从请求的Bearer token中解析当前用户信息。

    过程:
        1. 解码JWT，获取payload中的用户名字段；
        2. 如果解码失败或用户名不存在，抛出自定义异常；
        3. 根据用户名查询数据库获取用户对象，如果不存在，抛出异常；
        4. 返回用户对象。

    参数:
        token (str): HTTP Authorization请求头中的Bearer token，FastAPI自动传入

    返回:
        User对象: 当前请求对应的用户对象
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
    except Exception as e:
        logging.error(f"token中包含的用户信息异常，请检查token生成流程:{traceback.format_exc()}")
        raise CustomErrorThrowException(ErrorCode.TOKEN_PAYLOAD_INVALID)
    user = await get_user(username)
    if user is None:
        logging.error(f"用户信息获取异常")
        raise CustomErrorThrowException(ErrorCode.USER_NOT_FOUND)
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    """
    FastAPI依赖函数，判断当前用户是否处于激活状态。

    过程:
        1. 接收已解析的当前用户对象；
        2. 判断用户状态字段（status）是否为1，非1则视为非激活；
        3. 如果状态异常，抛出自定义异常；
        4. 返回当前激活用户对象。

    参数:
        current_user (User): 由 get_current_user 依赖函数注入的当前用户对象

    返回:
        User对象: 当前激活的用户对象
    """
    if current_user.status != 1:
        logging.error(f"用户信息状态异常:{traceback.format_exc()}")
        raise CustomErrorThrowException(ErrorCode.USER_STATUS_INVALID)
    return current_user








