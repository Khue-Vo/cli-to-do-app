"""This module provides the CLI To-Do model-controller."""
# clitodo/clitodo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from clitodo import DB_READ_ERROR, ID_ERROR
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

    def set_done(self, todo_id: int) -> CurrentToDo:
        """Set a to-do as done."""
        read = self._db_handler.read_todos() #Read all the to-dos
        if read.error: #Check if any error occurs during the reading
            return CurrentToDo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1] #Catch invalid to-do IDs that translate to invalid indices in the underlying to-do list
        except IndexError:
            return CurrentToDo({}, ID_ERROR)
        todo["Done"] = True #Set the to-do as done
        write = self._db_handler.write_todos(read.todo_list) #Write the update back to the database
        return CurrentToDo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentToDo:
        """Remove a to-do from the database using its id or index."""
        read = self._db_handler.read_todos() #Read the to-do list from the database
        if read.error: #Checks if any error occurs during the reading process
            return CurrentToDo({}, read.error)
        try: #Catch any invalid ID coming from the user’s input
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentToDo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list) #Write the updated to-do list back to the database
        return CurrentToDo(todo, write.error)

    def remove_all(self) -> CurrentToDo:
        """Remove all to-dos from the database."""
        write = self._db_handler.write_todos([])
        return CurrentToDo({}, write.error)