from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://redis:6379/0"
    broker_url: str = "redis://redis:6379/1"
    result_backend: str = "redis://redis:6379/2"
    app_name: str = "Disney Bot"
    debug: bool = False

    model_config = {
        "env_file": ".env"
    }


settings = Settings()
