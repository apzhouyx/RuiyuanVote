from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str
    
    # Redis配置
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: str
    
    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # 应用配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "小区投票统计系统"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 