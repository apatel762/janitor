import os
from pathlib import Path

import pytest

from janitor.notes import Note
from janitor.notes import NoteLink
from janitor.notes import NoteSerialisationError


def test_note__serialise__no_checksum_throws_error() -> None:
    note: Note = Note(Path("./notes/note1.md"))

    with pytest.raises(NoteSerialisationError) as exc_info:
        note.serialise()

    assert f"{repr(note)} has no SHA-256 checksum recorded." in exc_info.value.args[0]
    assert "Was the checksum calculated before serialisation?" in exc_info.value.args[0]


def test_note__serialise__no_path_throws_error() -> None:
    # noinspection PyTypeChecker
    note: Note = Note(None)
    note.sha256_checksum = "wow_where_did_this_checksum_come_from_94290342"

    with pytest.raises(NoteSerialisationError) as exc_info:
        note.serialise()

    assert f"{repr(note)} has no Path associated with it." in exc_info.value.args[0]
    assert "Something has gone horribly wrong..." in exc_info.value.args[0]


def test_note__serialise__returns_expected_info() -> None:
    note: Note = Note(Path("./notes/note1.md"))
    note.sha256_checksum = "my_really_accurate_checksum_123548534085473"
    note_json: dict = note.serialise()

    assert "sha256" in note_json.keys()
    assert "path" in note_json.keys()
    assert "links" in note_json.keys()
    assert "back" in note_json["links"]
    assert "forward" in note_json["links"]

    assert note_json["sha256"] == note.sha256_checksum
    assert note_json["path"] == os.path.abspath(note.path)
    assert len(note_json["links"]["back"]) == 0
    assert len(note_json["links"]["forward"]) == 0


def test_note__hash__when_note_has_no_path() -> None:
    # noinspection PyTypeChecker
    note: Note = Note(None)

    assert hash(note) == hash(None)


def test_note__hash__when_note_has_path() -> None:
    note: Note = Note(Path("./notes/note1.md"))

    assert hash(note) == hash(note.path)


def test_note__repr__contains_file_name() -> None:
    note: Note = Note(Path("./notes/note1.md"))

    assert repr(note) == "Note[note1.md]"


def test_note__repr__works_when_path_is_none() -> None:
    # noinspection PyTypeChecker
    note: Note = Note(None)

    assert repr(note) == "Note[None]"


def test_notelink__serialise__throws_error_when_origin_path_is_none() -> None:
    origin: Note = Note(Path("./notes/note1.md"))
    note_link: NoteLink = NoteLink(origin, "note context", "note2.md")
    note_link.origin.path = None

    with pytest.raises(NoteSerialisationError) as exc_info:
        note_link.serialise()

    assert (
        "Cannot serialise NoteLink when self.origin.path is None"
        in exc_info.value.args[0]
    )


def test_notelink__serialise__throws_error_when_origin_is_none() -> None:
    # noinspection PyTypeChecker
    note_link: NoteLink = NoteLink(None, "note context", "note2.md")

    with pytest.raises(NoteSerialisationError) as exc_info:
        note_link.serialise()

    assert (
        "Cannot serialise NoteLink when self.origin is None" in exc_info.value.args[0]
    )


def test_notelink__serialise__returns_expected_info() -> None:
    origin: Note = Note(Path("./notes/note1.md"))
    note_link: NoteLink = NoteLink(origin, "note context", "note2.md")
    note_link_json: dict = note_link.serialise()

    assert "origin" in note_link_json.keys()
    assert "destination" in note_link_json.keys()
    assert "context" in note_link_json.keys()

    assert note_link_json["origin"] == note_link.origin.path.name
    assert note_link_json["destination"] == note_link.destination_file_name
    assert note_link_json["context"] == note_link.origin_context


def test_notelink__hash__works() -> None:
    origin: Note = Note(Path("./notes/note1.md"))
    note_link: NoteLink = NoteLink(origin, "note context", "note2.md")

    assert hash(note_link) == hash(
        (note_link.origin, note_link.origin_context, note_link.destination_file_name)
    )


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
