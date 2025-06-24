import os
from pydantic_settings import BaseSettings, SettingsConfigDict


DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'fast_api'
DB_USER = 'lisoon'
DB_PASSWORD = '12345'


def get_db_url():
    return (f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@"
            f"{DB_HOST}:{DB_PORT}/{DB_NAME}")