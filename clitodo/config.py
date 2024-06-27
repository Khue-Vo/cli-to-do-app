"""This module provides the CLI To-Do config funtionality"""
# clitodo/config.py

import configparser #This module provides the ConfigParser class, which allows you to handle config files with a structure similar to INI files
from pathlib import Path #This class provides a cross-platform way to handle system paths

import typer

from clitodo import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__)) #Hold the path to the app's directory
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini" #Hold the path to the configuration file itself

def init_app(db_path: str) -> int:
    """Initialize the application.""" #Initialize the application's configuration file and database
    config_code = _init_config_file()
    if config_code != SUCCESS: #Check if an error occurs during the creation of the directory and configuration file
        return config_code #Return the error code
    database_code = _create_database(db_path)
    if database_code != SUCCESS: #Check if an error occurs during the creation of the database
        return database_code #Return the corresponding error code
    return SUCCESS

def _init_config_file() -> int: #Helper function
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True) #Create the configuration directory
    except OSError:
        return DIR_ERROR #Return the error code if something wrong happens during the creation of the directory
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True) #Create the configuration file
    except OSError:
        return FILE_ERROR #Return the error code if something wrong happens during the creation of the file
    return SUCCESS

def _create_database(db_path: str) -> int: #Helper function, creates the to-do database
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR #Return the appropriate error code if something wrong happens while creating the database
    return SUCCESS