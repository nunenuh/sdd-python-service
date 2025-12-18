"""
Health CLI commands.

This module provides command-line interface commands for health check operations.
Commands are organized here to keep them close to the health module while maintaining
separation from the REST API handlers.
"""

from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from fastapi_service.core.config import get_settings
from fastapi_service.core.logging import setup_logging
from fastapi_service.modules.health.usecase import HealthUseCase

# Initialize console for rich output
console = Console()

# Create health subcommand group
health_app = typer.Typer(help="Health check commands")


@health_app.command("ping")
def health_ping():
    """Simple ping endpoint for liveness checks."""
    setup_logging()
    console.print("[bold]Pinging service...[/bold]")

    # Simple ping response
    timestamp = datetime.now()
    console.print(f"[bold green]✓[/bold green] Service is alive")
    console.print(f"Status: [green]ok[/green]")
    console.print(f"Message: [cyan]pong[/cyan]")
    console.print(f"Timestamp: [yellow]{timestamp.isoformat()}[/yellow]")


@health_app.command("status")
def health_status():
    """Get basic health status with dependency checks."""
    setup_logging()
    console.print("[bold]Checking service health status...[/bold]")

    try:
        usecase = HealthUseCase()
        overall_status, components, uptime = usecase.get_basic_health()
        settings = get_settings()

        # Format uptime
        uptime_hours = int(uptime // 3600)
        uptime_minutes = int((uptime % 3600) // 60)
        uptime_seconds = int(uptime % 60)
        uptime_str = f"{uptime_hours}h {uptime_minutes}m {uptime_seconds}s"

        # Create status table
        status_table = Table(
            title="Service Health Status",
            show_header=True,
            header_style="bold magenta",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Overall Status", overall_status.upper())
        status_table.add_row("Version", settings.APP_VERSION)
        status_table.add_row("Uptime", uptime_str)
        status_table.add_row("Timestamp", datetime.now().isoformat())

        console.print("\n")
        console.print(status_table)

        # Components table
        if components:
            components_table = Table(
                title="Component Health",
                show_header=True,
                header_style="bold blue",
            )
            components_table.add_column("Component", style="cyan")
            components_table.add_column("Status", style="green")
            components_table.add_column("Message", style="yellow")
            components_table.add_column("Response Time", style="magenta")

            for component in components:
                status_color = "green" if component.status == "healthy" else "red"
                response_time = (
                    f"{component.response_time_ms:.2f} ms"
                    if component.response_time_ms
                    else "N/A"
                )
                components_table.add_row(
                    component.name.upper(),
                    f"[{status_color}]{component.status.upper()}[/{status_color}]",
                    component.message or "N/A",
                    response_time,
                )

            console.print("\n")
            console.print(components_table)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Health check failed: {str(e)}")
        raise typer.Exit(code=1)


@health_app.command("detailed")
def health_detailed():
    """Get comprehensive health status with system metrics."""
    setup_logging()
    console.print("[bold]Fetching detailed health status...[/bold]")

    try:
        usecase = HealthUseCase()
        (
            overall_status,
            components,
            system_metrics,
            process_metrics,
            system_info,
            uptime,
        ) = usecase.get_detailed_health()
        settings = get_settings()

        # Format uptime
        uptime_hours = int(uptime // 3600)
        uptime_minutes = int((uptime % 3600) // 60)
        uptime_seconds = int(uptime % 60)
        uptime_str = f"{uptime_hours}h {uptime_minutes}m {uptime_seconds}s"

        # Overall status table
        status_table = Table(
            title="Service Health Status",
            show_header=True,
            header_style="bold magenta",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Overall Status", overall_status.upper())
        status_table.add_row("Version", settings.APP_VERSION)
        status_table.add_row("Environment", settings.APP_ENVIRONMENT)
        status_table.add_row("Debug Mode", "ON" if settings.APP_DEBUG else "OFF")
        status_table.add_row("Uptime", uptime_str)
        status_table.add_row("Timestamp", datetime.now().isoformat())

        console.print("\n")
        console.print(status_table)

        # Components table
        if components:
            components_table = Table(
                title="Component Health",
                show_header=True,
                header_style="bold blue",
            )
            components_table.add_column("Component", style="cyan")
            components_table.add_column("Status", style="green")
            components_table.add_column("Message", style="yellow")
            components_table.add_column("Response Time", style="magenta")

            for component in components:
                status_color = "green" if component.status == "healthy" else "red"
                response_time = (
                    f"{component.response_time_ms:.2f} ms"
                    if component.response_time_ms
                    else "N/A"
                )
                components_table.add_row(
                    component.name.upper(),
                    f"[{status_color}]{component.status.upper()}[/{status_color}]",
                    component.message or "N/A",
                    response_time,
                )

            console.print("\n")
            console.print(components_table)

        # System metrics table
        system_table = Table(
            title="System Metrics",
            show_header=True,
            header_style="bold green",
        )
        system_table.add_column("Metric", style="cyan")
        system_table.add_column("Value", style="green")

        system_table.add_row("CPU Usage", f"{system_metrics.cpu_percent:.1f}%")
        system_table.add_row("Memory Usage", f"{system_metrics.memory_percent:.1f}%")
        system_table.add_row(
            "Memory Available", f"{system_metrics.memory_available_gb:.2f} GB"
        )
        system_table.add_row("Disk Usage", f"{system_metrics.disk_usage_percent:.1f}%")
        system_table.add_row("Disk Free", f"{system_metrics.disk_free_gb:.2f} GB")
        system_table.add_row(
            "Network Sent",
            f"{system_metrics.network_bytes_sent / (1024**2):.2f} MB",
        )
        system_table.add_row(
            "Network Received",
            f"{system_metrics.network_bytes_recv / (1024**2):.2f} MB",
        )

        console.print("\n")
        console.print(system_table)

        # Process metrics table
        process_table = Table(
            title="Process Metrics",
            show_header=True,
            header_style="bold yellow",
        )
        process_table.add_column("Metric", style="cyan")
        process_table.add_column("Value", style="green")

        process_table.add_row("Process ID", str(process_metrics.pid))
        process_table.add_row("Memory RSS", f"{process_metrics.memory_rss_mb:.2f} MB")
        process_table.add_row("Memory VMS", f"{process_metrics.memory_vms_mb:.2f} MB")
        process_table.add_row("CPU Usage", f"{process_metrics.cpu_percent:.1f}%")
        process_table.add_row("Threads", str(process_metrics.num_threads))
        process_table.add_row("Uptime", f"{process_metrics.uptime_seconds:.0f} seconds")
        process_table.add_row("Open Files", str(process_metrics.open_files))

        console.print("\n")
        console.print(process_table)

        # System info table
        info_table = Table(
            title="System Information",
            show_header=True,
            header_style="bold cyan",
        )
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="green")

        info_table.add_row("Python Version", system_info.python_version)
        info_table.add_row("Platform", system_info.platform)
        info_table.add_row("Hostname", system_info.hostname)
        info_table.add_row(
            "Boot Time", system_info.boot_time.strftime("%Y-%m-%d %H:%M:%S")
        )
        if system_info.load_average:
            load_avg_str = ", ".join(f"{load:.2f}" for load in system_info.load_average)
            info_table.add_row("Load Average", load_avg_str)

        console.print("\n")
        console.print(info_table)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Detailed health check failed: {str(e)}")
        raise typer.Exit(code=1)


def get_health_app() -> typer.Typer:
    """Get the health Typer app for registration in main CLI."""
    return health_app
