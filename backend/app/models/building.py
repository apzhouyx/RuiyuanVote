from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    building_number = Column(String(10), unique=True, index=True)  # 楼栋号
    unit_count = Column(Integer)  # 单元数
    floor_count = Column(Integer)  # 实际楼层数
    units_per_floor = Column(Integer)  # 每层户数
    total_units = Column(Integer)  # 总户数
    is_special = Column(Boolean, default=False)  # 是否特殊户型

    # 关联户型
    units = relationship("Unit", back_populates="building")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    unit_number = Column(String(10))  # 单元号
    floor = Column(Integer)  # 楼层
    room_number = Column(String(10))  # 房号
    has_voted = Column(Boolean, default=False)  # 是否已投票
    
    # 关联楼栋
    building = relationship("Building", back_populates="units") 