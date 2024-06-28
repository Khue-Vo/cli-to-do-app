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
            f""" with priority: {priority}""",
            fg=typer.colors.GREEN,
        )

@app.command(name="list") #Define list_all() as a Typer command using the @app.command(),
                          #The name argument to this decorator sets a custom name for the command, which is list here
                          #Doesn't take any argument or option, just lists the to-dos when user runs list from the command line
def list_all() -> None:
    """List all to-dos."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list() #Gets the to-do list from the database
    if len(todo_list) == 0: #A conditional statement to check if there’s at least one to-do in the list
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True) #Prints a top-level header to present the to-do list
    """Define and print the required columns to display the to-do list in a tabular format"""
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1): #Print every single to-do on its own row with appropriate padding and separators
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) -2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE) #Prints a line of dashes  to visually separate the to-do list from the next command-line prompt

@app.command(name="complete") #Define set_done() as a Typer command with the @app.command() decorator
def set_done(todo_id:  int = typer.Argument(...)) -> None:
    """Complete a to-do by setting it as done using its TODO_ID"""
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id) #Sets the to-do with the specific todo_id as done
    if error: #Checks if any error occurs during the process
        typer.secho(
            f'Completing to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do # {todo_id} "{todo['Description']}" completed!""",
            fg=typer.colors.GREEN,
        )

@app.command() #Define remove() asa Typer CLI command
def remove(
        todo_id: int = typer.Argument(...),
        force: bool = typer.Option(
            False,
            "--force",
            "-f",
            help="Force deletion without confirmation.",
        ), #Defines force as an option for the remove command
           #Allows user to delete a to-do without confirmation
) -> None:
    """Remove a to-do using its TODO_ID."""
    todoer = get_todoer()

    def _remove(): #Define an inner function
                   #Helper function that allows you to reuse the remove functionality
        todo ,error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing to-do # {todo_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""to-do # {todo_id}: '{todo["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )
    if force: #Checks the value of force.
              #If True, the user wants to remove the to-do without confirmation
        _remove()
    else:
        todo_list =todoer.get_todo_list() #Get the entire to-do list from the database
        try: #Retrieves the desired to-do from the list
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho("Invalid TODO_ID", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete to-do # {todo_id}: {todo['Description']}?"
        ) #Call Typer’s confirm() and store the result in delete.
          #This function provides an alternative way to ask for confirmation.
          #It allows to use a dynamically created confirmation prompt
        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")

@app.command(name="clear") #Define remove_all() as a Typer command using the @app.command() decorator with clear as the command name
def remove_all(
        force: bool = typer.Option(
            ...,
            prompt="Delete all to-dos?",
            help="Force deletion without confirmations",
        ), #Define force as a Typer Option
) -> None:
    """Remove all to-dos."""
    todoer = get_todoer()
    if force: #Checks if force is True
              #If so, remove all the to-dos from the database
        error = todoer.remove_all().error
        if error: #Check if something go wrong during the removing process
            typer.secho(
                f'Removing to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho("All to-dos were removed", fg=typer.colors.GREEN)
    else:
        typer.echo("Operation canceled")

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