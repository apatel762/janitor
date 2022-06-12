from pathlib import Path

from janitor.notes import Note


def test_note__repr__contains_file_name() -> None:
    note: Note = Note(Path("./notes/note1.md"))

    assert repr(note) == "Note[note1.md]"


def test_note__repr__works_when_path_is_none() -> None:
    # noinspection PyTypeChecker
    note: Note = Note(None)

    assert repr(note) == "Note[None]"
