"""
Main CLI entry point using Typer.

Typer is created by the same author as FastAPI and provides a modern,
type-hinted CLI framework that integrates well with FastAPI projects.

This module serves as the main entry point that registers commands from
various modules, following the same separation of concerns pattern as
the REST API handlers.
"""

import typer

from fastapi_service.cli.base import console
from fastapi_service.core.config import get_settings

# Initialize Typer app (disable Rich help to avoid compatibility issues)
app = typer.Typer(
    name="fastapi-service",
    help="FastAPI Service CLI - Command-line interface for FastAPI Service",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="none",  # Disable Rich markup for help to avoid compatibility issues
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def version():
    """Show application version."""
    settings = get_settings()
    console.print(f"[bold green]FastAPI Service[/bold green] v{settings.APP_VERSION}")


# Register module commands
# Each module can provide its own CLI commands via cli/commands.py
# This keeps commands organized by domain while maintaining separation of concerns

# Weather module commands
try:
    from fastapi_service.modules.weather.cli.commands import get_weather_app

    app.add_typer(get_weather_app(), name="weather")
except ImportError:
    # Module not available or doesn't have CLI commands
    pass

# Health module commands
try:
    from fastapi_service.modules.health.cli.commands import get_health_app

    app.add_typer(get_health_app(), name="health")
except ImportError:
    # Module not available or doesn't have CLI commands
    pass

# Quotes module commands
try:
    from fastapi_service.modules.quotes.cli.commands import get_quotes_app

    app.add_typer(get_quotes_app(), name="quotes")
except ImportError:
    # Module not available or doesn't have CLI commands
    pass


def main():
    """Main CLI entry point."""
    import sys

    # Handle Rich compatibility issue only for help command
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
        try:
            app()
        except (TypeError, AttributeError) as e:
            if "make_metavar" in str(e) or "ctx" in str(e):
                # Fallback: Use Click directly for help
                import click

                click.echo("FastAPI Service CLI")
                click.echo("\nAvailable commands:")
                click.echo("  version              Show application version")
                click.echo("  weather              Weather-related commands")
                click.echo("    current            Get current weather")
                click.echo("    forecast           Get weather forecast")
                click.echo("  health               Health check commands")
                click.echo("    ping               Simple liveness check")
                click.echo("    status             Basic health status")
                click.echo("    detailed           Detailed health with metrics")
                click.echo("  quotes               Quotes-related commands")
                click.echo("    random             Get a random quote")
                click.echo("    get                Get a quote by ID")
                click.echo("    search             Search quotes with filters")
                click.echo("    author             Get quotes by author")
                click.echo("\nUse 'cli <command> --help' for more information")
                sys.exit(0)
            raise
    else:
        # Normal command execution
        app()


if __name__ == "__main__":
    main()
