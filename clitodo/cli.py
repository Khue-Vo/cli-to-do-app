"""This module provides the CLI To-Do List"""
# clitodo/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from clitodo import (
    ERRORS, __app_name__, __version__, config, database, clitodo
)

app = typer.Typer() #Create an explicit Typer application

@app.command() #Define init() as a Typer command using the @app.command()
def init( #Define a Typer Option instance and assign it as a default value to db_path
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="to-do database location?" #Displays a prompt asking for the database location,
                                              # also allows the user to accept the default path by pressing Enter
        )
)-> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path) #Create the application's configuration file and to-do database
    if app_init_error: #Check if the call to init_app() returns an error
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path)) #Initialize the database with an empty to-do list
    if db_init_error: #Check if the call to init_database() returns an error
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)

def get_todoer() -> clitodo.Todoer:
    if config.CONFIG_FILE_PATH.exists(): # Define a conditional that checks if the application's configuration file exist
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Confid file not found. Please, run "clitodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists(): #Check if the path to the database exists
        return clitodo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "clitodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()  # Define add() as a Typer command using the @app.command()
def add(
        description: List[str] = typer.Argument(...), #Define description as an argument to add(),
                                                      #user must provide a to-do description at the command line
        priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error: #A conditional statement that prints an error message and exits the application if an error occurs while adding the new to-do to the database
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added"""
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )

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