from sqlalchemy.orm import Session
from app.models.building import Building, Unit
from app.core.config import settings

# 初始化楼栋数据
def init_buildings(db: Session):
    # 普通楼栋（1,3,4,5,6,7,8栋）
    normal_buildings = [1, 3, 4, 5, 6, 7, 8]
    for number in normal_buildings:
        building = Building(
            building_number=str(number),
            unit_count=1,
            floor_count=32,  # 2-33层
            units_per_floor=3,
            total_units=96,
            is_special=False
        )
        db.add(building)
        db.flush()  # 获取ID
        
        # 创建单元
        for floor in range(2, 34):  # 2-33层
            for room in range(1, 4):  # 每层3户
                unit = Unit(
                    building_id=building.id,
                    unit_number="1",
                    floor=floor,
                    room_number=f"{floor:02d}{room:02d}",
                    has_voted=False
                )
                db.add(unit)

    # 2栋（双单元）
    building_2 = Building(
        building_number="2",
        unit_count=2,
        floor_count=32,  # 2-33层
        units_per_floor=8,
        total_units=256,
        is_special=False
    )
    db.add(building_2)
    db.flush()

    # 创建2栋单元
    for unit in range(1, 3):  # 2个单元
        for floor in range(2, 34):  # 2-33层
            for room in range(1, 5):  # 每单元4户
                unit_obj = Unit(
                    building_id=building_2.id,
                    unit_number=str(unit),
                    floor=floor,
                    room_number=f"{floor:02d}{room:02d}",
                    has_voted=False
                )
                db.add(unit_obj)

    # 9栋
    building_9 = Building(
        building_number="9",
        unit_count=1,
        floor_count=31,  # 2-32层
        units_per_floor=3,
        total_units=93,
        is_special=False
    )
    db.add(building_9)
    db.flush()

    # 创建9栋单元
    for floor in range(2, 33):  # 2-32层
        for room in range(1, 4):  # 每层3户
            unit = Unit(
                building_id=building_9.id,
                unit_number="1",
                floor=floor,
                room_number=f"{floor:02d}{room:02d}",
                has_voted=False
            )
            db.add(unit)

    # 10栋（双单元）
    building_10 = Building(
        building_number="10",
        unit_count=2,
        floor_count=31,  # 2-32层
        units_per_floor=8,
        total_units=248,
        is_special=False
    )
    db.add(building_10)
    db.flush()

    # 创建10栋单元
    for unit in range(1, 3):  # 2个单元
        for floor in range(2, 33):  # 2-32层
            for room in range(1, 5):  # 每单元4户
                unit_obj = Unit(
                    building_id=building_10.id,
                    unit_number=str(unit),
                    floor=floor,
                    room_number=f"{floor:02d}{room:02d}",
                    has_voted=False
                )
                db.add(unit_obj)

    # 11栋
    building_11 = Building(
        building_number="11",
        unit_count=1,
        floor_count=30,  # 2-31层
        units_per_floor=4,
        total_units=120,
        is_special=False
    )
    db.add(building_11)
    db.flush()

    # 创建11栋单元
    for floor in range(2, 32):  # 2-31层
        for room in range(1, 5):  # 每层4户
            unit = Unit(
                building_id=building_11.id,
                unit_number="1",
                floor=floor,
                room_number=f"{floor:02d}{room:02d}",
                has_voted=False
            )
            db.add(unit)

    # 特殊户型（12-17栋）
    special_buildings = range(12, 18)
    for number in special_buildings:
        is_double_unit = number in [12, 13, 15, 17]  # 双单元楼栋
        unit_count = 2 if is_double_unit else 1
        total_units = 24 if is_double_unit else 12

        building = Building(
            building_number=str(number),
            unit_count=unit_count,
            floor_count=7,  # 1-7层
            units_per_floor=2,  # 简化处理
            total_units=total_units,
            is_special=True
        )
        db.add(building)
        db.flush()

        # 创建特殊户型单元
        for unit in range(1, unit_count + 1):
            # 1-2层合并：4户/单元
            for room in range(1, 5):
                unit_obj = Unit(
                    building_id=building.id,
                    unit_number=str(unit),
                    floor=1,
                    room_number=f"01{room:02d}",
                    has_voted=False
                )
                db.add(unit_obj)

            # 3-5层：每层2户/单元
            for floor in range(3, 6):
                for room in range(1, 3):
                    unit_obj = Unit(
                        building_id=building.id,
                        unit_number=str(unit),
                        floor=floor,
                        room_number=f"{floor:02d}{room:02d}",
                        has_voted=False
                    )
                    db.add(unit_obj)

            # 6-7层合并：2户/单元
            for room in range(1, 3):
                unit_obj = Unit(
                    building_id=building.id,
                    unit_number=str(unit),
                    floor=6,
                    room_number=f"06{room:02d}",
                    has_voted=False
                )
                db.add(unit_obj)

    db.commit()

def init_db(db: Session):
    # 初始化楼栋数据
    init_buildings(db) 