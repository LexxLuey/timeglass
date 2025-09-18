"""TimeGlass CLI application."""

import typer
from timeglass import __version__

app = typer.Typer()


@app.command()
def ui():
    """Start the TimeGlass web dashboard."""
    typer.echo("Starting TimeGlass dashboard...")
    # Placeholder: implement dashboard server
    typer.echo("Dashboard available at http://localhost:8000")


@app.callback()
def main(version: bool = typer.Option(False, "--version", help="Show version")):
    """TimeGlass - A lightweight profiling tool for FastAPI applications."""
    if version:
        typer.echo(f"TimeGlass {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
