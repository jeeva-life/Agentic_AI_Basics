import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 2000
    
    # Application Configuration
    APP_NAME: str = "YouTube Multi-Agent Content Workflow"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Content Processing Limits
    MAX_TRANSCRIPT_LENGTH: int = 10000
    MAX_CONTENT_LENGTH: int = 5000
    MAX_TITLE_LENGTH: int = 100
    
    # Platform-specific Settings
    LINKEDIN_CHAR_LIMIT: int = 3000
    TWITTER_CHAR_LIMIT: int = 280
    BLOG_MIN_LENGTH: int = 300
    
    # SEO Settings
    MIN_SEO_SCORE: int = 70
    TARGET_READABILITY_SCORE: int = 60
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]
    ALLOWED_METHODS: list = ["GET", "POST", "PUT", "DELETE"]
    ALLOWED_HEADERS: list = ["*"]
    
    # Logging Configuration
    LOG_FILE: Optional[str] = None
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Workflow Configuration
    WORKFLOW_TIMEOUT: int = 300  # 5 minutes
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Content Generation Settings
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: list = ["en", "es", "fr", "de", "it", "pt"]
    
    # YouTube API Settings
    YOUTUBE_API_KEY: Optional[str] = None
    YOUTUBE_TRANSCRIPT_TIMEOUT: int = 30
    
    # Error Handling
    SHOW_DETAILED_ERRORS: bool = False
    
    # Additional fields that might be in .env
    reload: Optional[bool] = None
    langchain_tracing_v2: Optional[str] = None
    secret_key: Optional[str] = None
    cors_origins: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env

# Create global settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that required settings are configured"""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file or environment variables.")
    
    if not settings.OPENAI_MODEL:
        raise ValueError("OPENAI_MODEL is required.")

# Validate settings on import
try:
    validate_settings()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file or environment variables.") 