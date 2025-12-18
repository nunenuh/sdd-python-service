# CLI Commands

This package provides command-line interface (CLI) commands for the FastAPI Service using **Typer**.

## Why Typer?

- **Created by FastAPI author** - Same philosophy and design principles
- **Type-hinted** - Uses Python type hints for automatic validation
- **Modern** - Built on Click but with better developer experience
- **Rich output** - Integrates with Rich library for beautiful terminal output

## Installation

After installing dependencies:

```bash
make install
```

The CLI is available via Poetry:

```bash
poetry run cli --help
```

Or install the package and use directly:

```bash
poetry install
fastapi-service --help
```

## Available Commands

### Version

```bash
poetry run cli version
```

### Weather Commands

#### Current Weather

```bash
# Basic usage (latitude and longitude are positional arguments)
poetry run cli weather current 52.52 13.41

# With custom timezone
poetry run cli weather current 52.52 13.41 --tz "Europe/Berlin"
```

#### Weather Forecast

```bash
# Full forecast (hourly + daily)
poetry run cli weather forecast 52.52 13.41

# Only daily forecast (exclude hourly)
poetry run cli weather forecast 52.52 13.41 --no-hourly

# Only hourly forecast (exclude daily)
poetry run cli weather forecast 52.52 13.41 --no-daily

# No forecasts, only current weather
poetry run cli weather forecast 52.52 13.41 --no-hourly --no-daily

# Custom timezone
poetry run cli weather forecast 52.52 13.41 --tz "Europe/Berlin"
```

**Note**: Latitude and longitude are positional arguments (required), timezone and forecast flags are options.

## Adding New Commands

1. Create a new function with `@app.command()` decorator
2. Use Typer options/arguments for parameters
3. Reuse existing use cases/services from modules
4. Use Rich console for beautiful output

Example:

```python
@app.command()
def my_command(
    param: str = typer.Option(..., help="Parameter description"),
):
    """Command description."""
    console.print(f"[bold green]Executing: {param}[/bold green]")
    # Your logic here
```

## Benefits of CLI vs REST API

### Use CLI when:
- **Automation** - Scripts, cron jobs, CI/CD pipelines
- **Local development** - Quick testing without HTTP server
- **Batch operations** - Processing multiple items
- **System integration** - Direct system calls

### Use REST API when:
- **Web applications** - Browser-based interfaces
- **Mobile apps** - Mobile client integration
- **Microservices** - Service-to-service communication
- **Public API** - External consumers

## Architecture

The CLI follows the same separation of concerns pattern as the REST API:

### Structure

```
cli/
├── main.py          # Main entry point, registers module commands
├── base.py          # Shared CLI utilities
└── README.md        # This file

modules/{module}/
└── cli/
    ├── __init__.py
    └── commands.py  # Module-specific CLI commands
```

### Command Flow

The CLI reuses the same business logic as the REST API:
- **CLI Command** (`modules/{module}/cli/commands.py`) → **Use Case** → **Service** → **External API**

This ensures consistency between CLI and REST API responses.

### Separation of Concerns

- **`cli/main.py`**: Main entry point that registers commands from all modules
- **`cli/base.py`**: Shared utilities (console helpers, common functions)
- **`modules/{module}/cli/commands.py`**: Module-specific commands, organized by domain

This structure mirrors the API organization:
- API: `modules/{module}/apiv1/handler.py` → HTTP endpoints
- CLI: `modules/{module}/cli/commands.py` → CLI commands

Both use the same UseCase → Service → Repository layers underneath.

## Adding New Module Commands

### Step 1: Create Module Command File

Create `src/fastapi_service/modules/{module}/cli/commands.py`:

```python
"""Module CLI commands."""

import typer
from fastapi_service.cli.base import console
from fastapi_service.modules.{module}.usecase import ModuleUseCase

# Create subcommand group
module_app = typer.Typer(help="Module description")

@module_app.command("action")
def module_action(
    param: str = typer.Argument(..., help="Parameter description"),
):
    """Command description."""
    console.print(f"[bold]Executing action with {param}...[/bold]")
    # Use your use case here
    usecase = ModuleUseCase()
    # ... your logic

def get_module_app() -> typer.Typer:
    """Get the module Typer app for registration in main CLI."""
    return module_app
```

### Step 2: Register in Main CLI

Add to `src/fastapi_service/cli/main.py`:

```python
# Register module commands
try:
    from fastapi_service.modules.{module}.cli.commands import get_module_app
    app.add_typer(get_module_app(), name="{module}")
except ImportError:
    pass
```

### Step 3: Create `__init__.py`

Create `src/fastapi_service/modules/{module}/cli/__init__.py`:

```python
"""Module CLI commands."""
```

## Benefits of This Structure

1. **Separation of Concerns**: Each module owns its CLI commands
2. **Scalability**: Easy to add new modules without cluttering main.py
3. **Consistency**: Mirrors the API handler structure
4. **Maintainability**: Commands are co-located with their related modules
5. **Testability**: Module commands can be tested independently

