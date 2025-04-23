import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base_class import Base
from app.db.init_db import init_db
from app.models.building import Building, Unit  # 导入所有模型

def init():
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL.rsplit('/', 1)[0])  # 去掉数据库名
    
    try:
        # 创建数据库
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.DATABASE_URL.rsplit('/')[-1]}"))
    except Exception as e:
        print(f"创建数据库失败: {e}")
        sys.exit(1)

    # 连接到新创建的数据库
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 创建会话
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 初始化数据
        init_db(db)
        
        print("数据库初始化成功！")
    except Exception as e:
        print(f"初始化数据失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init() 