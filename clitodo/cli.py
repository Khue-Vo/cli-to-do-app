"""This module provides the CLI To-Do List"""
# clitodo/cli.py

from typing import Optional

import typer

from clitodo import __app_name__, __version__

app = typer.Typer() #Create an explicit Typer application

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application' version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return