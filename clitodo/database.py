"""This module provides the CLI To-Do database functionality."""
# clitodo/database.py

import configparser #This module provides the ConfigParser class, which allows you to handle config files with a structure similar to INI files
import json
from pathlib import Path #This class provides a cross-platform way to handle system paths
from typing import Any, Dict, List, NamedTuple

from clitodo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." +Path.home().stem + "_todo.json"
) # Create a holder for the default database file path
  # The application will use this path if the user doesn't provide a custom one

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])# The "General" key represents the file section that stores the required information
                                                     # The "database" key retireves tha database path

def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]") #Empty to-do list, the list initializes the JSON database
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]] #The to-do list users will write and read from the database
    error: int #An integer number representing a return code related to the current database operation

class DatabaseHandler: #Allow users to read and write data to the to-do database using the json module from the standard library
    def __init__(self, db_path: Path) -> None: #Define class initializer
        self._db_path = db_path

    def read_todos(self) -> DBResponse: #This method reads the to-do list from tha database and deserializes it
        try: #Catch any errors that occur while users are opening the database
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError: #Catch wrong JSON format
                    return DBResponse([], DB_READ_ERROR)
        except OSError: #Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse: #Take a list of to-do dictionaries and write it to the database
        try: #Catch any errors that occur while users are opening the database
            with self._db_path.open("w") as db: #Open the database for writing
                json.dump(todo_list, db, indent=4) #Dump the to-do list as a JSON payload into the database
            return DBResponse(todo_list, SUCCESS)
        except OSError: #Catch file IO problems
            return DBResponse(todo_list, DB_WRITE_ERROR)