from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    BOT_TOKEN: str
    WEATHER_API_KEY: str
    ADMINS: list[int]
    DEFAULT_LANGUAGE: str = "ru"

    @validator("ADMINS", pre=True)
    def parse_admins(cls, v):
        if isinstance(v, str):
            return [int(i.strip()) for i in v.strip('[]').split(",")]
        return v

    class Config:
        env_file = ".env"

settings = Settings()