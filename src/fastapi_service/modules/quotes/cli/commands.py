"""
Quotes CLI commands.

This module provides command-line interface commands for quotes-related operations.
Commands are organized here to keep them close to the quotes module while maintaining
separation from the REST API handlers.
"""

import asyncio

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from fastapi_service.core.logging import setup_logging
from fastapi_service.modules.quotes.usecase import QuotesUseCase

# Initialize console for rich output
console = Console()

# Create quotes subcommand group
quotes_app = typer.Typer(help="Quotes-related commands")


@quotes_app.command("random")
def quotes_random(
    tags: str = typer.Option(None, "--tags", help="Comma-separated tags to filter by"),
    max_length: int = typer.Option(None, "--max-length", help="Maximum quote length"),
):
    """Get a random quote."""
    setup_logging()
    console.print("[bold]Fetching random quote...[/bold]")

    async def fetch_quote():
        usecase = QuotesUseCase()
        quote = await usecase.get_random_quote(tags=tags, max_length=max_length)

        # Create a rich panel for the quote
        quote_text = f'"{quote.content}"'
        author_text = f"— {quote.author}"

        panel = Panel(
            f"{quote_text}\n\n[dim]{author_text}[/dim]",
            title="[bold cyan]Random Quote[/bold cyan]",
            border_style="cyan",
        )

        console.print("\n")
        console.print(panel)

        if quote.tags:
            tags_str = ", ".join(quote.tags)
            console.print(f"\n[dim]Tags: {tags_str}[/dim]")
        console.print(f"[dim]Length: {quote.length} characters[/dim]\n")

    asyncio.run(fetch_quote())


@quotes_app.command("get")
def quotes_get(quote_id: str = typer.Argument(..., help="Quote ID")):
    """Get a specific quote by ID."""
    setup_logging()
    console.print(f"[bold]Fetching quote {quote_id}...[/bold]")

    async def fetch_quote():
        try:
            usecase = QuotesUseCase()
            quote = await usecase.get_quote_by_id(quote_id)

            # Create a rich panel for the quote
            quote_text = f'"{quote.content}"'
            author_text = f"— {quote.author}"

            panel = Panel(
                f"{quote_text}\n\n[dim]{author_text}[/dim]",
                title=f"[bold cyan]Quote #{quote.id}[/bold cyan]",
                border_style="cyan",
            )

            console.print("\n")
            console.print(panel)

            if quote.tags:
                tags_str = ", ".join(quote.tags)
                console.print(f"\n[dim]Tags: {tags_str}[/dim]")
            console.print(f"[dim]Length: {quote.length} characters[/dim]\n")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

    asyncio.run(fetch_quote())


@quotes_app.command("search")
def quotes_search(
    query: str = typer.Option(None, "--query", help="Search query string"),
    author: str = typer.Option(None, "--author", help="Filter by author name"),
    tags: str = typer.Option(None, "--tags", help="Comma-separated tags"),
    min_length: int = typer.Option(None, "--min-length", help="Minimum quote length"),
    max_length: int = typer.Option(None, "--max-length", help="Maximum quote length"),
    limit: int = typer.Option(10, "--limit", help="Number of quotes to return"),
    skip: int = typer.Option(0, "--skip", help="Number of quotes to skip"),
):
    """Search for quotes with filters."""
    setup_logging()
    console.print("[bold]Searching quotes...[/bold]")

    async def search_quotes():
        usecase = QuotesUseCase()
        quotes, total_count = await usecase.search_quotes(
            query=query,
            author=author,
            tags=tags,
            min_length=min_length,
            max_length=max_length,
            limit=limit,
            skip=skip,
        )

        if not quotes:
            console.print("[yellow]No quotes found.[/yellow]")
            return

        # Create a rich table for quotes
        table = Table(
            title=f"Quotes (showing {len(quotes)} of {total_count})",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("#", style="cyan", width=4)
        table.add_column("Quote", style="green", width=60)
        table.add_column("Author", style="yellow", width=20)
        table.add_column("Tags", style="blue", width=20)

        for i, quote in enumerate(quotes, start=skip + 1):
            # Truncate long quotes
            quote_text = (
                quote.content[:57] + "..." if len(quote.content) > 60 else quote.content
            )
            tags_str = ", ".join(quote.tags[:3]) if quote.tags else "—"
            if len(tags_str) > 20:
                tags_str = tags_str[:17] + "..."

            table.add_row(str(i), quote_text, quote.author, tags_str)

        console.print("\n")
        console.print(table)
        console.print(f"\n[dim]Total: {total_count} quotes[/dim]\n")

    asyncio.run(search_quotes())


@quotes_app.command("author")
def quotes_author(
    author_slug: str = typer.Argument(..., help="Author slug"),
    limit: int = typer.Option(10, "--limit", help="Number of quotes to return"),
    skip: int = typer.Option(0, "--skip", help="Number of quotes to skip"),
):
    """Get quotes by author slug."""
    setup_logging()
    console.print(f"[bold]Fetching quotes by {author_slug}...[/bold]")

    async def fetch_quotes():
        usecase = QuotesUseCase()
        quotes, total_count = await usecase.get_quotes_by_author(
            author_slug=author_slug, limit=limit, skip=skip
        )

        if not quotes:
            console.print("[yellow]No quotes found for this author.[/yellow]")
            return

        # Create a rich table for quotes
        table = Table(
            title=f"Quotes by {author_slug} (showing {len(quotes)} of {total_count})",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("#", style="cyan", width=4)
        table.add_column("Quote", style="green", width=70)
        table.add_column("Tags", style="blue", width=20)

        for i, quote in enumerate(quotes, start=skip + 1):
            # Truncate long quotes
            quote_text = (
                quote.content[:67] + "..." if len(quote.content) > 70 else quote.content
            )
            tags_str = ", ".join(quote.tags[:3]) if quote.tags else "—"
            if len(tags_str) > 20:
                tags_str = tags_str[:17] + "..."

            table.add_row(str(i), quote_text, tags_str)

        console.print("\n")
        console.print(table)
        console.print(f"\n[dim]Total: {total_count} quotes[/dim]\n")

    asyncio.run(fetch_quotes())


def get_quotes_app() -> typer.Typer:
    """Get the quotes Typer app for registration in main CLI."""
    return quotes_app

