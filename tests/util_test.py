from pathlib import Path

from janitor import util


def test_get_cache_directory():
    result: Path = util.get_cache_directory()

    assert ".cache" and "janitor" in str(result)


def test_get_tmp_directory():
    result: Path = util.get_tmp_directory()

    assert ".cache" and "janitor" and "tmp" in str(result)
