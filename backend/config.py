from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    app_name: str = "Luxe v4.0 - AI Helpdesk"
    debug: bool = False

    # Database (SQLite for local dev, PostgreSQL for production)
    database_url: str = "sqlite:///./ai_customer_support.db"

    # Clerk
    clerk_secret_key: str = "sk_test_placeholder"
    clerk_publishable_key: str = "pk_test_placeholder"

    # Stripe (optional, added later)
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Frontend
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
