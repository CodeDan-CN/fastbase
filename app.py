import logging
import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from exception.all_exception import global_exception_handlers
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
    _app.include_router(router=user, prefix="/v1/user", tags=["user"])

    # SQLite 数据源路径
    sqlite_db_path = "./db/app.db"  # 替换为你的 SQLite 数据库路径

    # 注册 SQLite 数据源
    register_tortoise(
        _app,
        db_url=f"sqlite://{sqlite_db_path}",
        modules={'models': ['entity.database.sqlite']},  # 替换成你定义的模型路径
        generate_schemas=True,  # 若首次初始化需要建表可打开
        add_exception_handlers=True,
    )

    @_app.on_event("startup")
    async def app_startup():
        os.makedirs("logs", exist_ok=True)

        # 清除旧的 handler，防止重复添加
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("logs/app.log", mode='a', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logging.info("fastapi run------------------ Starting")

    @_app.on_event("shutdown")
    async def shutdown_event():
        logging.info("fastapi run------------------ ending")

    return _app

# app = create_app()  # 正式环境切换

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host=os.environ.get('SERVER_HOST', '0.0.0.0'), port=int(os.environ.get('SERVER_PORT', 8000)))
