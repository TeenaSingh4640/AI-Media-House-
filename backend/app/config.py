from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "AI-Native News Platform"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database - use SQLite by default for local dev
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_news.db")
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:8000"]
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # LLM APIs
    CLAUDE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Vector Database
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-west1-gcp"
    PINECONE_INDEX: str = "ai-news"
    
    # News Sources
    ET_API_KEY: str = ""
    NEWS_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
