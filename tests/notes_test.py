from pathlib import Path

from janitor.notes import Note


def test_note__when_created__repr_string_metadata() -> None:
    note: Note = Note(Path("./test.md"))

    assert repr(note) == "Note[test.md bl=0,fl=0,sha256=no]"
