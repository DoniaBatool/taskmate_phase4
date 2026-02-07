"""Health check endpoints for container orchestration."""

from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, text

from src.db import get_session, engine
from src.schemas import HealthResponse, SimpleHealthResponse

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)


@router.get("/health", response_model=SimpleHealthResponse)
async def health_check():
    """
    Liveness probe - is the service running?

    This endpoint checks if the FastAPI service is alive and responding.
    It does NOT check database connectivity (that's /ready).

    Returns:
        SimpleHealthResponse: Simple status indicating service is alive
    """
    return SimpleHealthResponse(status="healthy")


@router.get("/ready", response_model=HealthResponse)
async def readiness_check(session: Session = Depends(get_session)):
    """
    Readiness probe - is the service ready to accept traffic?

    This endpoint verifies the service can handle requests by checking:
    - Database connectivity
    - Connection pool health

    Returns:
        HealthResponse: System status including database connectivity and pool metrics

    Raises:
        HTTPException: 503 if database is unavailable
    """
    try:
        # Simple query to test connection
        session.exec(text("SELECT 1"))
        database_status = "connected"
        overall_status = "ready"

        # Get connection pool status for monitoring
        pool_status = engine.pool.status()
        logger.info(f"Pool health: {pool_status}")

    except Exception as e:
        database_status = "disconnected"
        overall_status = "not_ready"
        pool_status = None
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Database not ready: {str(e)}",
        ) from e

    return HealthResponse(
        status=overall_status,
        database=database_status,
        version="1.0.0",
        timestamp=datetime.utcnow(),
        pool_status=pool_status
    )

