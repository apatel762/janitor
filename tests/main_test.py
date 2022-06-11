from typer.testing import CliRunner

from janitor.main import app

runner = CliRunner()


def test_scan__when_invalid_folder__aborts() -> None:
    result = runner.invoke(
        app, ["scan", "~/i/really/hope/this/folder/doesnt/exist/djbfksjfsk"]
    )

    assert result.exit_code == 2


def test_scan__when_continue__begins_scan() -> None:
    result = runner.invoke(app, ["scan", ".", "--force-index-rebuild"], input="y\n")

    assert "Will index folder:" in result.stdout
    assert "Would you like to continue? [y/N]: y\n" in result.stdout
    assert "Starting scan..." in result.stdout
    assert result.exit_code == 0


def test_scan__when_do_not_continue__app_aborts() -> None:
    result = runner.invoke(app, ["scan", "."], input="n\n")

    assert result.exit_code == 1
