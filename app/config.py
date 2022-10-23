from pydantic import BaseSettings


class Settings(BaseSettings):
    work_dir: str = 'static/upload/'

settings = Settings()
