import logging
import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.db_config import init_db
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

    @_app.on_event("startup")
    async def app_startup():
        await init_db()
        logging.info("fastapi run------------------ Starting")

    @_app.on_event("shutdown")
    async def shutdown_event():
        logging.info("fastapi run------------------ ending")

    return _app

# app = create_app()  # 正式环境切换

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host=os.environ.get('SERVER_HOST', '0.0.0.0'), port=int(os.environ.get('SERVER_PORT', 8000)))
