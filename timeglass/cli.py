"""TimeGlass CLI application."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from timeglass import __version__
from timeglass.web import start_dashboard

console = Console()
app = typer.Typer()


@app.command()
def ui(
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind the server to"),
    port: int = typer.Option(8000, "--port", help="Port to bind the server to"),
    db_path: str = typer.Option("timeglass.db", "--db", help="Path to the database file"),
):
    """Start the TimeGlass web dashboard."""
    console.print()
    console.print(
        Panel.fit(
            "[bold blue]TimeGlass Dashboard[/bold blue]",
            title="🚀 Starting Server",
            border_style="blue",
        )
    )

    try:
        console.print(f"[green]✓[/green] Starting dashboard on http://{host}:{port}")
        console.print(f"[green]✓[/green] Using database: {db_path}")
        console.print()

        start_dashboard(host=host, port=port, db_path=db_path)

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]✗ Error starting dashboard: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def version():
    """Show TimeGlass version."""
    version_text = Text(f"TimeGlass {__version__}", style="bold magenta")
    console.print(version_text)


@app.command()
def stats(db_path: str = typer.Option("timeglass.db", "--db", help="Path to the database file")):
    """Show profiling statistics summary."""
    from timeglass.storage import TimeGlassStorage

    try:
        storage = TimeGlassStorage(db_path)
        summary = storage.get_stats_summary()

        console.print()
        console.print(
            Panel.fit(
                "[bold green]Profiling Statistics[/bold green]",
                title="📊 Summary",
                border_style="green",
            )
        )

        console.print(f"[cyan]Total Requests:[/cyan] {summary['total_requests']:,}")
        console.print(f"[cyan]Avg Duration:[/cyan] {summary['avg_duration_ms']:.2f}ms")
        console.print(f"[cyan]Max Duration:[/cyan] {summary['max_duration_ms']:.2f}ms")
        console.print(f"[cyan]Min Duration:[/cyan] {summary['min_duration_ms']:.2f}ms")
        console.print(f"[cyan]Avg CPU Usage:[/cyan] {summary['avg_cpu_percent']:.1f}%")
        console.print(
            f"[cyan]Avg Memory Usage:[/cyan] {summary['avg_memory_percent']:.1f}%"
        )
        console.print(
            f"[cyan]Current CPU:[/cyan] {summary['current_cpu_percent']:.1f}%"
        )
        console.print(
            f"[cyan]Current Memory:[/cyan] {summary['current_memory_percent']:.1f}%"
        )
        console.print()

    except Exception as e:
        console.print(f"[red]✗ Error retrieving statistics: {e}[/red]")
        raise typer.Exit(1)


@app.callback()
def main():
    """TimeGlass - A lightweight profiling tool for FastAPI applications."""
    pass


if __name__ == "__main__":
    app()
