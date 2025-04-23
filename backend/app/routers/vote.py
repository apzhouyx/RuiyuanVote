from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.building import Unit
from app.schemas.vote import VoteCreate, VoteResponse
from app.routers.websocket import broadcast_vote_update

router = APIRouter()

@router.post("/{unit_id}", response_model=VoteResponse)
async def submit_vote(
    unit_id: int,
    db: Session = Depends(get_db)
):
    """提交投票"""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="找不到该单元")
    
    if unit.has_voted:
        raise HTTPException(status_code=400, detail="该单元已经投过票")
    
    # 更新投票状态
    unit.has_voted = True
    db.commit()
    
    # 广播更新
    await broadcast_vote_update({
        "building_id": unit.building_id,
        "unit_id": unit.id,
        "status": "voted"
    })
    
    return {"success": True, "message": "投票成功"}

@router.get("/statistics", response_model=dict)
def get_vote_statistics(db: Session = Depends(get_db)):
    """获取投票统计信息"""
    total_units = db.query(Unit).count()
    voted_units = db.query(Unit).filter(Unit.has_voted == True).count()
    
    return {
        "total": total_units,
        "voted": voted_units,
        "percentage": round(voted_units / total_units * 100, 2) if total_units > 0 else 0
    } 