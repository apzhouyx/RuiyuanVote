from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                # 如果发送失败，移除连接
                self.active_connections.remove(connection)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 等待消息
            data = await websocket.receive_text()
            # 广播消息给所有连接
            await manager.broadcast(json.loads(data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def broadcast_vote_update(data: dict):
    """广播投票更新信息"""
    await manager.broadcast(data) 