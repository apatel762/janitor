from pathlib import Path

from janitor.notes import Note
from janitor.notes import NoteLink


def test_note__repr__contains_file_name() -> None:
    note: Note = Note(Path("./notes/note1.md"))

    assert repr(note) == "Note[note1.md]"


def test_note__repr__works_when_path_is_none() -> None:
    # noinspection PyTypeChecker
    note: Note = Note(None)

    assert repr(note) == "Note[None]"


def test_notelink__repr__shows_file_names() -> None:
    origin: Note = Note(Path("./notes/note1.md"))
    note_link: NoteLink = NoteLink(origin, "note context", "note2.md")

    assert (
        repr(note_link)
        == f"NoteLink[{note_link.origin.path.name} -> {note_link.destination_file_name}]"
    )


def test_notelink__repr__works_when_destination_file_name_is_empty() -> None:
    origin: Note = Note(Path("./notes/note1.md"))
    note_link: NoteLink = NoteLink(origin, "note context", "")

    assert repr(note_link) == f"NoteLink[{note_link.origin.path.name} -> ]"


def test_notelink__repr__works_when_destination_file_name_is_none() -> None:
    origin: Note = Note(Path("./notes/note1.md"))
    # noinspection PyTypeChecker
    note_link: NoteLink = NoteLink(origin, "note context", None)

    assert repr(note_link) == f"NoteLink[{note_link.origin.path.name} -> None]"


def test_notelink__repr__works_when_origin_path_is_none() -> None:
    # noinspection PyTypeChecker
    origin: Note = Note(None)
    note_link: NoteLink = NoteLink(origin, "note context", "note2.md")

    assert repr(note_link) == f"NoteLink[None -> {note_link.destination_file_name}]"


def test_notelink__repr__works_when_origin_is_none() -> None:
    # noinspection PyTypeChecker
    note_link: NoteLink = NoteLink(None, "note context", "note2.md")

    assert repr(note_link) == f"NoteLink[None -> {note_link.destination_file_name}]"
