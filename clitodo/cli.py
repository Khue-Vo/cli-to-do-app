"""This module provides the CLI To-Do List"""
# clitodo/cli.py

import sqlite3
from pathlib import Path
from typing import List, Optional
from tabulate import tabulate

import typer

from clitodo import (
    SUCCESS, DB_WRITE_ERROR, ERRORS, __app_name__, __version__
)

app = typer.Typer() #Create an explicit Typer application
my_todo = 'my_todo.db'

@app.command() #Define init() as a Typer command using the @app.command()
def init() -> None:
    """Initialize the to-do database."""
    try:
        conn = sqlite3.connect(my_todo)
        conn.execute('''CREATE TABLE IF NOT EXISTS TODO_LIST
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PRIORITY INT NOT NULL,
                DONE TEXT DEFAULT 'False',
                DESCRIPTION TEXT NOT NULL);''')
        conn.close()
        typer.secho(f"The to-do database is C:\\Users\\Khue Vo\\training\\python\\cli-to-do-app\\my_todo.db", fg=typer.colors.GREEN)
    except sqlite3.Error as e:
        typer.secho(f"Error during initialization process: {e}", fg=typer.colors.RED)

@app.command()  # Define add() as a Typer command using the @app.command()
def add(description: List[str] = typer.Argument(...), #Define description as an argument to add(),
                                                      #user must provide a to-do description at the command line
        priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),):
    """Add a new to-do with a DESCRIPTION."""
    conn = sqlite3.connect(my_todo)
    cursor = conn.cursor()
    try:
        description_text = " ".join(description)
        sql = '''INSERT INTO TODO_LIST (PRIORITY, DESCRIPTION) VALUES (?,?)'''
        data = (priority, description_text)
        cursor.execute(sql, data)
        conn.commit()
        return typer.secho(
            f"""to-do: "{description_text}" was added"""
            f""" with priority: {priority}""",
            fg=typer.colors.GREEN,
        )
    except sqlite3.Error as e:
        typer.secho(
            f'Adding to-do failed with "{e}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    finally:
        conn.close()


@app.command(name="list") #Define list_all() as a Typer command using the @app.command(),
                          #The name argument to this decorator sets a custom name for the command, which is list here
                          #Doesn't take any argument or option, just lists the to-dos when user runs list from the command line
def list_all() -> None:
    """List all to-dos."""
    conn = sqlite3.connect(my_todo)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM TODO_LIST")
        todo_list = cursor.fetchall()
        if len(todo_list) == 0:  # Check if there’s at least one to-do in the list
            typer.secho(
                "There are no tasks in the to-do list yet", fg=typer.colors.RED
            )
            raise typer.Exit()
        typer.secho("\nto-do list:\n", fg=typer.colors.BLUE,
                    bold=True)  # Prints a top-level header to present the to-do list
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
        for todo in todo_list:
            id_, priority, done, description = todo
            typer.secho(
                f"{id_}{(len(columns[0]) - len(str(id_))) * ' '}"
                f"| {priority}{(len(columns[1]) - len(str(priority)) - 4) * ' '}"
                f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
                f"| {description}",
                fg=typer.colors.BLUE            )
        typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
    except sqlite3.Error as e:
        typer.secho(
            f'Displaying to-do list failed with "{e}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    finally:
        conn.close()

@app.command(name="complete") #Define set_done() as a Typer command with the @app.command() decorator
def set_done(todo_id:  int = typer.Argument(...)) -> None:
    """Complete a to-do by setting it as done using its TODO_ID"""
    conn = sqlite3.connect(my_todo)
    try:
        conn.execute("UPDATE TODO_LIST set DONE = 'True' where PRIORITY = ?", (todo_id,))
        conn.commit()
        typer.secho(f'To-do updated successfully', fg=typer.colors.GREEN)
    except sqlite3.Error as e:
        typer.secho(
            f'Updating to-do failed with "{e}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    finally:
        conn.close()


# @app.command() #Define remove() asa Typer CLI command
# def remove(todo_id:  int = typer.Argument(...)):
#     """Remove a to-do using its TODO_ID."""
#     conn = sqlite3.connect(my_todo)
#     try:
#         conn.execute("DELETE from TODO_LIST where PRIORITY = ?", (todo_id,))
#         conn.commit()
#         typer.secho(f'To-do removed successfully', fg=typer.colors.GREEN)
#     except sqlite3.Error as e:
#         typer.secho(
#             f'Removing to-do failed with "{e}"', fg=typer.colors.RED
#         )
#         raise typer.Exit(1)
#     finally:
#         conn.close()
#
#
# @app.command(name="clear") #Define remove_all() as a Typer command using the @app.command() decorator with clear as the command name
# def remove_all():
#     """Remove all to-dos."""
#     conn = sqlite3.connect(my_todo)
#     try:
#         conn.execute("DROP TABLE IF EXISTS TODO_LIST")
#         conn.commit()
#         conn.execute('''CREATE TABLE IF NOT EXISTS TODO_LIST
#                         (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                         PRIORITY INT NOT NULL,
#                         DONE TEXT DEFAULT 'False',
#                         DESCRIPTION TEXT NOT NULL);''')
#         typer.secho(f'Clearing all to-do successfully')
#     except sqlite3.Error as e:
#         typer.secho(
#             f'Clearing all to-do failed with "{e}"', fg=typer.colors.RED
#         )
#         raise typer.Exit(1)
#     finally:
#         conn.close()

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