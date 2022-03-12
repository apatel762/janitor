import pytest

from janitor.typerutils import warn


def test_warn__with_None__raises_error() -> None:
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        warn(None)


def test_warn__with_empty_string__raises_error() -> None:
    with pytest.raises(RuntimeError):
        warn("")


def test_warn__with_valid_text__returns_text_with_yellow_prefix() -> None:
    text: str = "Hello"
    assert warn(text) == f"\x1b[33m\x1b[1mWARN\x1b[0m: {text}"
