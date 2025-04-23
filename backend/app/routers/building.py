from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.building import Building, Unit
from app.schemas.building import BuildingCreate, BuildingResponse, UnitCreate, UnitResponse
from app.routers.websocket import broadcast_vote_update

router = APIRouter()

@router.get("/", response_model=List[BuildingResponse])
def get_all_buildings(db: Session = Depends(get_db)):
    """获取所有楼栋信息"""
    return db.query(Building).all()

@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(building_id: int, db: Session = Depends(get_db)):
    """获取特定楼栋信息"""
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="楼栋不存在")
    return building

@router.post("/", response_model=BuildingResponse)
def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    """创建新楼栋"""
    db_building = Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

@router.get("/{building_id}/units", response_model=List[UnitResponse])
def get_building_units(building_id: int, db: Session = Depends(get_db)):
    """获取楼栋下所有单元信息"""
    return db.query(Unit).filter(Unit.building_id == building_id).all()

@router.post("/{building_id}/reset")
async def reset_building_votes(building_id: int, db: Session = Depends(get_db)):
    """重置楼栋的所有投票数据"""
    # 检查楼栋是否存在
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="楼栋不存在")
    
    try:
        # 重置该楼栋所有单元的投票状态
        db.query(Unit).filter(Unit.building_id == building_id).update({"has_voted": False})
        db.commit()
        
        # 广播更新
        await broadcast_vote_update({
            "building_id": building_id,
            "type": "reset",
            "message": "重置成功"
        })
        
        return {"success": True, "message": "重置成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"重置失败: {str(e)}") 