from typer.testing import CliRunner

from janitor.main import app

runner = CliRunner()


def test_scan():
    result = runner.invoke(app, ["scan"])
    assert result.exit_code == 0
    assert "Done scanning" in result.stdout
