import logging
import os
import traceback
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from config.logging_config import init_daily_logger
from config.setting import settings
from exception.all_exception import global_exception_handlers
from exception.custom_exception import CustomErrorThrowException
from exception.error_codes import ErrorCode
from utils.milvus_client import EmbeddingMilvusClient
from models.client.llm_client import LLMClient
from web.login_web import login
from web.user_web import user


def create_app():
    _app = FastAPI(
        title="digital portrait service",
        version="v1.0.1",
        # 全局以及自定义异常捕获
        exception_handlers=global_exception_handlers
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 添加路由
    _app.include_router(router=login, prefix="/v1/auth", tags=["auth"])
    _app.include_router(router=user, prefix="/v1/user", tags=["user"])

    # 假设你用 pymysql 作为驱动
    register_tortoise(
        _app,
        db_url=f"mysql://{settings.mysql['user']}:{settings.mysql['password']}@{settings.mysql['host']}:{settings.mysql['port']}/{settings.mysql['database']}?charset=utf8mb4",
        modules={'models': ['entity.database.mysql']},  # 改成你自己的模型路径
        # generate_schemas=True,  # 是否自动生成表结构（生产环境建议关闭）
        add_exception_handlers=True,
        generate_schemas=True,  # 启用自动建表
    )

    @_app.on_event("startup")
    async def app_startup():
        try:
            init_daily_logger()
            logging.info("初始化大模型")
            LLMClient.init({
                "model": settings.llm_default["model"],
                "deployment_type": settings.llm_default["deployment_type"],
                "temperature": settings.llm_default["temperature"],
                "max_token": settings.llm_default["max_token"],
                "base_url": settings.llm_default["base_url"]
            })
            logging.info("初始化milvus连接")
            EmbeddingMilvusClient.configure(**{
                "host": settings.milvus["host"],
                "port": settings.milvus["port"],
                "user": settings.milvus["user"],
                "password": settings.milvus["password"],
                "db_name": settings.milvus["db_name"],
            })
            logging.info("fastapi run------------------ Starting")
        except Exception:
            logging.error(f"startup 阶段初始化失败：{traceback.format_exc()}")
            raise CustomErrorThrowException(ErrorCode.SYSTEM_INIT_ERROR)

    @_app.on_event("shutdown")
    async def shutdown_event():
        logging.info("fastapi run------------------ ending")

    return _app

# app = create_app()  # 正式环境切换

if __name__ == '__main__':
    # 初始化日志
    app = create_app()
    uvicorn.run(app, host=os.environ.get('SERVER_HOST', '0.0.0.0'), port=int(os.environ.get('SERVER_PORT', 8003)))