"""This module provides the CLI To-Do List"""
# clitodo/cli.py

from typing import Optional

import typer

from clitodo import __app_name__, __version__

app = typer.Typer() #Create an explicit Typer application

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}") #Prints the application name and version
        raise typer.Exit() #Raises an exception to exit the application

@app.callback() #Define main() as a Typer callback using the @app.callback() decorator
def main(
        #Define version, which is of type Optional[bool]
        version: Optional[bool] = typer.Option(
            #The first argument to the initializer of Option
            None,
            #Set the command-line names for the version option
            "--version",
            "-v",
            #Provides a help message for the version option
            help="Show the application' version and exit.",
            #Attaches a callbcak function to the version option, running the option automatically calls the function
            callback=_version_callback,
            #Tells Typer that the version command-line option has precedence over commands in the current application
            is_eager=True,
        )
) -> None:
    return