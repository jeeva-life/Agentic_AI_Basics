"""
Routes package for FastAPI application.
Contains organized route handlers for different endpoints.
"""

from . import workflow, health

__all__ = ["workflow", "health"]