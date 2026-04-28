from pydantic_settings import BaseSettings
from environs import Env

env = Env()
env.read_env()

class Settings(BaseSettings):
    MONGO_URI: str = env('MONGO_URI')
    CLASE2_URL: str = env('CLASE2_URL')
    DB_NAME: str = "Parcial1_2025"

settings = Settings()