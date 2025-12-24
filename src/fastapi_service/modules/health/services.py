"""
Health check services and business logic for FastAPI service.

This module contains the core business logic for health monitoring,
separated from HTTP handling concerns.
"""

import os
import platform
import sys
import time
from datetime import datetime
from typing import List, Tuple

import psutil

from ...core.config import get_settings
from ...core.logging import get_logger
from .schemas import ComponentHealth, ProcessMetrics, SystemInfo, SystemMetrics

logger = get_logger(__name__)

# Track service start time for uptime calculation
SERVICE_START_TIME = time.time()


class ComponentHealthService:
    """Service for checking individual component health."""

    @staticmethod
    def check_database() -> ComponentHealth:
        """Check database connectivity."""
        start_time = time.time()
        settings = get_settings()
        try:
            # Basic check - can be enhanced with actual DB connection
            if settings.DB_HOST and settings.DB_NAME:
                response_time = (time.time() - start_time) * 1000
                return ComponentHealth(
                    name="database",
                    status="healthy",
                    message=f"Database configured: {settings.DB_HOST}/{settings.DB_NAME}",
                    response_time_ms=response_time,
                )
            else:
                response_time = (time.time() - start_time) * 1000
                return ComponentHealth(
                    name="database",
                    status="unhealthy",
                    message="Database not configured",
                    response_time_ms=response_time,
                )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return ComponentHealth(
                name="database",
                status="unhealthy",
                message=f"Database check failed: {str(e)}",
                response_time_ms=response_time,
            )

    @staticmethod
    def check_redis() -> ComponentHealth:
        """Check Redis connectivity."""
        start_time = time.time()
        settings = get_settings()
        try:
            if settings.REDIS_HOST:
                response_time = (time.time() - start_time) * 1000
                return ComponentHealth(
                    name="redis",
                    status="healthy",
                    message=f"Redis configured: {settings.REDIS_HOST}:{settings.REDIS_PORT}",
                    response_time_ms=response_time,
                )
            else:
                response_time = (time.time() - start_time) * 1000
                return ComponentHealth(
                    name="redis",
                    status="unhealthy",
                    message="Redis not configured",
                    response_time_ms=response_time,
                )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return ComponentHealth(
                name="redis",
                status="unhealthy",
                message=f"Redis check failed: {str(e)}",
                response_time_ms=response_time,
            )

class HealthService:
    """Main health service for aggregating health checks."""

    def __init__(self):
        """Initialize health service."""
        self.component_service = ComponentHealthService()

    def get_basic_health(
        self,
    ) -> Tuple[str, List[ComponentHealth], float]:
        """Get basic health status with component checks."""
        components = [
            self.component_service.check_database(),
            self.component_service.check_redis(),
        ]

        # Determine overall status
        overall_status = "healthy"
        for component in components:
            if component.status == "unhealthy":
                overall_status = "unhealthy"
                break

        uptime = time.time() - SERVICE_START_TIME
        return overall_status, components, uptime

    def get_detailed_health(
        self,
    ) -> Tuple[
        str, List[ComponentHealth], SystemMetrics, ProcessMetrics, SystemInfo, float
    ]:
        """Get detailed health status with system metrics."""
        # Get component health
        overall_status, components, uptime = self.get_basic_health()

        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        network = psutil.net_io_counters()

        system_metrics = SystemMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_available_gb=memory.available / (1024**3),
            disk_usage_percent=disk.percent,
            disk_free_gb=disk.free / (1024**3),
            network_bytes_sent=network.bytes_sent,
            network_bytes_recv=network.bytes_recv,
        )

        # Get process metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        process_metrics = ProcessMetrics(
            pid=process.pid,
            memory_rss_mb=process_memory.rss / (1024**2),
            memory_vms_mb=process_memory.vms / (1024**2),
            cpu_percent=process.cpu_percent(interval=0.1),
            num_threads=process.num_threads(),
            uptime_seconds=uptime,
            open_files=len(process.open_files()),
        )

        # Get system info
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        load_avg = os.getloadavg() if hasattr(os, "getloadavg") else None

        system_info = SystemInfo(
            python_version=sys.version.split()[0],
            platform=platform.platform(),
            hostname=platform.node(),
            boot_time=boot_time,
            load_average=list(load_avg) if load_avg else None,
        )

        return (
            overall_status,
            components,
            system_metrics,
            process_metrics,
            system_info,
            uptime,
        )


# Singleton instance
_health_service = None


def get_health_service() -> HealthService:
    """Get health service singleton instance."""
    global _health_service
    if _health_service is None:
        _health_service = HealthService()
    return _health_service
