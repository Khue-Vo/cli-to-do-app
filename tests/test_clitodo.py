# tests/test_clitodo.py

from typer.testing import CliRunner

from clitodo import __app_name__, __version__, cli

runner = CliRunner()

def test_version(): #Define first unit test for testing the application's version
    result = runner.invoke(cli.app, ["--version"]) #Run the application with the __version option,
                                                        #stop the result of this call in result
    assert result.exit_code == 0 #Assert that the application's exit code is equal to 0
                                 #to check that the application ran successfully
    assert f"{__app_name__} v{__version__}\n" in result.stdout #Assert that the application's version is present with the standard output,
