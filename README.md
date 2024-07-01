# TODO App CLI

Build a to-do app for the command line.

The application should have a user-friendly command-line interface that 
allows the users to interact with the app and manage their to-do lists.

# Requirements

The Model-View-Controller pattern

Command-line interfaces (CLI)

Python type hints, also known as type annotations

Unit tests with pytest

Object-oriented programming in Python

Configuration files with configparser

JSON files with Python's json

File system path manipulation with pathlib

# Installation

Use github to install and set up the project

```sh
git clone https://github.com/Khue-Vo/cli-to-do-app.git
```

## Navigate to the project directory
```sh
cd ...\cli-to-do-app
```

# Usage

Use the command-line interface(CLI) to operate the project

## Show the Help box
```sh
python -m clitodo --help
```

## Show version of the cli-to-do-app
```sh
python -m clitodo --version
```

## Create new to-do list
```sh
python -m clitodo init
```

## Add new to-do "Get some milk" with priority 1 
(priorty only range from 1 to 3)
```sh
python -m clitodo add Get some milk -p 1
```

## Add new to-do "Clean the house" with priority 3
```sh
python -m clitodo add Clean the house --priority 3
```

## Add new to-do "Wash the car" with default priority
```sh
python -m clitodo add Wash the car
```

## Show the to-do list
```sh
python -m clitodo list
```

## Set one to-do as complete by using its priority
```sh
python -m clitodo complete 1
```

## Remove one to-do out of the list by using its priority
```sh
python -m clitodo remove 2
```

## Clear the list
```sh
python -m clitodo clear
```
