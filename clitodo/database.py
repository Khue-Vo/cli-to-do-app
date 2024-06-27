"""This module provides the CLI To-Do database functionality."""
# clitodo/database.py

import configparser #This module provides the ConfigParser class, which allows you to handle config files with a structure similar to INI files
from pathlib import Path #This class provides a cross-platform way to handle system paths

from clitodo import DB_WRITE_ERROR, SUCCESS

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