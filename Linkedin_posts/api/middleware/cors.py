from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings

def setup_cors_middleware(app):
    """Setup CORS middleware with configuration"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"]
    )