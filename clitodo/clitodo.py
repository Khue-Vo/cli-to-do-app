"""This module provides the CLI To-Do model-controller."""
# clitodo/clitodo.py

from typing import  Any, Dict, NamedTuple

class CurrentToDo(NamedTuple): #Create a subclass of typing.NamedTuple with two fields
    todo: Dict[str, Any]
    error: int