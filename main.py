# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine


# 导入各模块路由
from app.routers import (
    user_router,
    device_router,
    usage_router,
    security_router,
    feedback_router,
    analytics_router
)



# 创建 FastAPI 应用实例
app = FastAPI(
    title="智能家居管理系统 API",
    version="1.0.0"
)

# 注册各模块路由
app.include_router(user_router.router)
app.include_router(device_router.router)
app.include_router(usage_router.router)
app.include_router(security_router.router)
app.include_router(feedback_router.router)
app.include_router(analytics_router.router)
