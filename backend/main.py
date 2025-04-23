from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import building, vote, websocket
from app.core.config import settings

app = FastAPI(title="小区投票统计系统")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(building.router, prefix="/api/buildings", tags=["buildings"])
app.include_router(vote.router, prefix="/api/votes", tags=["votes"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "小区投票统计系统API服务"} 