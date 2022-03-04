from typer.testing import CliRunner

from janitor.main import app

runner = CliRunner()


def test_scan():
    result = runner.invoke(app, ["scan"])
    assert result.exit_code == 0
    assert "I am done scanning for stuff to do" in result.stdout


def test_scan_verbose_has_extra_output():
    result = runner.invoke(app, ["scan", "--verbose"])
    assert result.exit_code == 0
    assert (
        "I am the janitor and I am about to look around for stuff to do"
        in result.stdout
    )
    assert "I am done scanning for stuff to do" in result.stdout
