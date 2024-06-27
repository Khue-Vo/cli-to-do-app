"""This module provides the CLI To-Do model-controller."""
# clitodo/clitodo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from clitodo import DB_READ_ERROR
from clitodo.database import DatabaseHandler

class CurrentToDo(NamedTuple): #Create a subclass of typing.NamedTuple with two fields
    todo: Dict[str, Any] #The dictionary holding the information for the current to-do
    error: int #The return or error code confirming if the current operation was successful or not

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler= DatabaseHandler(db_path) # Falitate direct communication with the to-do database

    def add(self, description: List[str], priority: int = 2) -> CurrentToDo:
        """Add a new to-do to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
            todo = {
                "Description": description_text,
                "Priority": priority,
                "Done": False,
            } #Build a new to do from user's input
            read = self._db_handler.read_todos() #Read the to-do list from the database
            if read.error == DB_READ_ERROR: #Check if .read_todos() returns a DB_READ_ERROR.
                return CurrentToDo(todo, read.error)
            read.todo_list.append(todo)
            write = self._db_handler.write_todos(read.todo_list) #Write the updated to-do list back to the database
            return CurrentToDo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos() #Get the entire to-do list from the database
        return read.todo_list