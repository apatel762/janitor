from typer.testing import CliRunner

from janitor.main import app

runner = CliRunner()


def test_scan__when_continue__begins_scan():
    result = runner.invoke(app, ["scan", "~/my/notes/folder"], input="y\n")

    assert "Will index folder: ~/my/notes/folder" in result.stdout
    assert "Would you like to continue? [y/N]: y\n" in result.stdout
    assert "Starting scan..." in result.stdout
    assert result.exit_code == 0


def test_scan__when_do_not_continue__app_aborts():
    result = runner.invoke(app, ["scan", "~/my/notes/folder"], input="n\n")

    assert result.exit_code == 1
