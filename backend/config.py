from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    app_name: str = "AI Customer Support"
    debug: bool = False

    # Database
    database_url: str

    # Clerk
    clerk_secret_key: str
    clerk_publishable_key: str

    # Stripe
    stripe_secret_key: str
    stripe_publishable_key: str

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Frontend
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
