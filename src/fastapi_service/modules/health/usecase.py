"""
Health use case orchestration layer.
"""

from typing import List, Tuple

from .schemas import ComponentHealth, ProcessMetrics, SystemInfo, SystemMetrics
from .services import HealthService, get_health_service


class HealthUseCase:
    """Use case for orchestrating health check operations."""

    def __init__(self):
        """Initialize health use case."""
        self.service = get_health_service()

    def get_basic_health(
        self,
    ) -> Tuple[str, List[ComponentHealth], float]:
        """Get basic health status with component checks.

        Returns:
            Tuple of (overall_status, components, uptime_seconds)
        """
        return self.service.get_basic_health()

    def get_detailed_health(
        self,
    ) -> Tuple[
        str, List[ComponentHealth], SystemMetrics, ProcessMetrics, SystemInfo, float
    ]:
        """Get detailed health status with system metrics.

        Returns:
            Tuple of (overall_status, components, system_metrics, process_metrics, system_info, uptime_seconds)
        """
        return self.service.get_detailed_health()
