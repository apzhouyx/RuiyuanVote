from pydantic import BaseModel
from typing import List, Optional

class UnitBase(BaseModel):
    unit_number: str
    floor: int
    room_number: str

class UnitCreate(UnitBase):
    building_id: int

class UnitResponse(UnitBase):
    id: int
    building_id: int
    has_voted: bool

    class Config:
        from_attributes = True

class BuildingBase(BaseModel):
    building_number: str
    unit_count: int
    floor_count: int
    units_per_floor: int
    total_units: int
    is_special: bool = False

class BuildingCreate(BuildingBase):
    pass

class BuildingResponse(BuildingBase):
    id: int
    units: List[UnitResponse] = []

    class Config:
        from_attributes = True 