from typer.testing import CliRunner
import helikite
import os

runner = CliRunner()


def test_cli_version():
    file_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(helikite.__file__)),
            os.pardir,
        )
    )
    # Get the version from the pyproject.toml file in the root directory
    with open(os.path.join(file_dir, "pyproject.toml"), "r") as f:
        pyproject = f.read()
        version = (
            pyproject.split("\n")[2].split("=")[1].strip().replace('"', "")
        )
    result = runner.invoke(helikite.app, ["--version"])
    assert result.exit_code == 0
    assert "helikite" in result.stdout
    assert version in result.stdout
