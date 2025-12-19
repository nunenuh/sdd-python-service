"""
Main API router that aggregates all service endpoints.
"""

from fastapi import APIRouter

from .modules.health.apiv1.handler import router as health_router

# Main API router
api_router = APIRouter()

# Include all module routers
api_router.include_router(health_router, prefix="/v1/health", tags=["Health"])

api_router.include_router(articles_router, prefix="/v1/articles", tags=["Articles"])
api_router.include_router(sources_router, prefix="/v1/sources", tags=["Sources"])
api_router.include_router(crawler_router, prefix="/v1/crawler", tags=["Crawler"])
