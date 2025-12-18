"""
Health check response schemas for the news crawler service.

This module defines Pydantic models for structuring health check responses,
ensuring consistent API response formats across all health endpoints.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    """Simple ping response for liveness checks."""

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Response timestamp")
    message: str = Field(..., description="Status message")


class ComponentHealth(BaseModel):
    """Health status of a service component."""

    name: str = Field(..., description="Component name")
    status: str = Field(..., description="Component status (healthy/unhealthy)")
    message: Optional[str] = Field(None, description="Status message or error details")
    response_time_ms: Optional[float] = Field(
        None, description="Component response time in milliseconds"
    )


class SystemMetrics(BaseModel):
    """System performance metrics."""

    cpu_percent: float = Field(..., description="CPU usage percentage")
    memory_percent: float = Field(..., description="Memory usage percentage")
    memory_available_gb: float = Field(..., description="Available memory in GB")
    disk_usage_percent: float = Field(..., description="Disk usage percentage")
    disk_free_gb: float = Field(..., description="Free disk space in GB")
    network_bytes_sent: int = Field(..., description="Network bytes sent")
    network_bytes_recv: int = Field(..., description="Network bytes received")


class ProcessMetrics(BaseModel):
    """Process-specific metrics."""

    pid: int = Field(..., description="Process ID")
    memory_rss_mb: float = Field(..., description="Resident memory in MB")
    memory_vms_mb: float = Field(..., description="Virtual memory in MB")
    cpu_percent: float = Field(..., description="Process CPU usage percentage")
    num_threads: int = Field(..., description="Number of threads")
    uptime_seconds: float = Field(..., description="Process uptime in seconds")
    open_files: int = Field(..., description="Number of open file descriptors")


class SystemInfo(BaseModel):
    """System information."""

    python_version: str = Field(..., description="Python version")
    platform: str = Field(..., description="Operating system platform")
    hostname: str = Field(..., description="System hostname")
    boot_time: datetime = Field(..., description="System boot time")
    load_average: Optional[List[float]] = Field(
        None, description="System load average (1, 5, 15 min)"
    )


class HealthStatusResponse(BaseModel):
    """Basic health status response with dependencies."""

    status: str = Field(..., description="Overall service status")
    timestamp: datetime = Field(..., description="Response timestamp")
    version: str = Field(..., description="Service version")
    components: List[ComponentHealth] = Field(
        ..., description="Component health statuses"
    )
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


class DetailedHealthResponse(BaseModel):
    """Comprehensive health response with system metrics."""

    status: str = Field(..., description="Overall service status")
    timestamp: datetime = Field(..., description="Response timestamp")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")

    # Component health
    components: List[ComponentHealth] = Field(
        ..., description="Component health statuses"
    )

    # System metrics
    system_metrics: SystemMetrics = Field(..., description="System performance metrics")
    process_metrics: ProcessMetrics = Field(..., description="Process-specific metrics")
    system_info: SystemInfo = Field(..., description="System information")

    # Additional context
    environment: str = Field(
        ..., description="Environment (development/staging/production)"
    )
    debug_mode: bool = Field(..., description="Debug mode status")
