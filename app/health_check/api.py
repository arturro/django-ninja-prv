import os
import platform
import time

from django.db import connection
from django.utils import timezone

from ninja import Router, Schema

SERVER_START_TIME = time.time()


def get_uptime():
    uptime_seconds = int(time.time() - SERVER_START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


router = Router()


class HealthCheckSchema(Schema):
    status: str
    message: str
    version: str
    uptime: str
    timestamp: str
    environment: str
    database: str


@router.get("/", response=HealthCheckSchema)
def health_check(request):
    """
    Health check endpoint to verify the API is running.
    """

    # Check database connection
    db_conn_status = "unknown"
    try:
        connection.ensure_connection()
        db_conn_status = "connected"
    except Exception as e:
        db_conn_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "message": "API is running",
        "version": "1.0.0",
        "platform": platform.platform(),  # example from copilot ;)
        "uptime": get_uptime(),
        "timestamp": timezone.now().isoformat(),
        "environment": os.getenv("DJANGO_ENV", "development"),
        "database": db_conn_status,
    }
