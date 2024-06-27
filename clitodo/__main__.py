"""CLI To-Do entry point script"""
# clitodo/__main__.py

from clitodo import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__) #Call the Typer app, passing the application's name to the prog_name argument,
                                    # ensure that the users get the correct app name when running the --help option on their command line

if __name__ == "__main__":
    main()
