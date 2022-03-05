from pathlib import Path

from janitor.notes import Note


def test_note__when_created__repr_string_shows_size():
    note: Note = Note(Path("./test.md"))

    assert repr(note) == "Note[test.md]"
