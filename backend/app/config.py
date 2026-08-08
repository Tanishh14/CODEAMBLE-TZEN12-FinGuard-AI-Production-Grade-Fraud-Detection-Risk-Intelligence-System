from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FinGuard AI"
    environment: str = "development"
    redis_url: str = "redis://localhost:6379/0"
    kafka_brokers: str = "localhost:9092"
    database_dsn: str = "postgresql://user:pass@localhost:5432/finguard"

    class Config:
        env_file = ".env"


settings = Settings()
