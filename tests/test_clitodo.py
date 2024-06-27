# tests/test_clitodo.py

import json

import pytest
from typer.testing import CliRunner

from clitodo import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    clitodo,
)

runner = CliRunner()

def test_version(): #Define first unit test for testing the application's version
    result = runner.invoke(cli.app, ["--version"]) #Run the application with the __version option,
                                                        #stop the result of this call in result
    assert result.exit_code == 0 #Assert that the application's exit code is equal to 0
                                 #to check that the application ran successfully
    assert f"{__app_name__} v{__version__}\n" in result.stdout #Assert that the application's version is present with the standard output,

@pytest.fixture #Decorator
def mock_json_file(tmp_path): #Create and return a temporary JSON file, db_file, with a single-item to-do list in it
    todo = [{"Description": "Get some milk.", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

#Some data to create the test cases
test_data1 = {
    "description": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    }
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    }
}

#Test function using parametrization in pytest
@pytest.mark.parametrize(
    "description, priority, expected", #Holds descriptive names for the two required parameters and also a descriptive return value name
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        )
    ]
)
def test_add(mock_json_file, description, priority, expected):
    todoer = clitodo.Todoer(mock_json_file)
    assert todoer.add(description, priority) == expected
    read = todoer._db_handler.read_todos()
    assert len(read.todo_list) == 2