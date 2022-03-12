import os.path
from pathlib import Path

import pytest

from janitor.indexer import Index
from janitor.indexer import NoteIndexerError
from janitor.notes import Note


def test_index__when_register_note__increases_size() -> None:
    index: Index = Index()

    assert len(index) == 0
    index.register(Note(Path()))
    assert len(index) == 1


def test_index__when_register_invalid_type__raises_error() -> None:
    index: Index = Index()

    with pytest.raises(NoteIndexerError):
        # noinspection PyTypeChecker
        index.register(None)


def test_index__serialise_has_correct_structure__with_empty_index() -> None:
    index: Index = Index()

    assert index.serialise() == {}


def test_index__serialise_has_correct_structure__with_populated_index() -> None:
    index: Index = Index()
    note: Note = Note(Path("./notes/note1.md"))
    note.sha256_checksum = "my-really-secure-checksum-123456789"
    index.register(note)

    index_as_json: dict = index.serialise()

    # only one note in the index
    assert len(index_as_json) == 1

    # the entry is keyed on the note's file name
    assert note.path.name in index_as_json

    # the entry has 3 values
    assert len(index_as_json[note.path.name]) == 3
    assert "links" in index_as_json[note.path.name]
    assert "path" in index_as_json[note.path.name]
    assert "sha256" in index_as_json[note.path.name]
    assert index_as_json[note.path.name]["path"] == os.path.abspath(note.path)
    assert index_as_json[note.path.name]["sha256"] == note.sha256_checksum

    # the link entry has 2 values, both empty
    assert len(index_as_json[note.path.name]["links"]) == 2
    assert "back" in index_as_json[note.path.name]["links"]
    assert "forward" in index_as_json[note.path.name]["links"]
    assert len(index_as_json[note.path.name]["links"]["back"]) == 0
    assert len(index_as_json[note.path.name]["links"]["forward"]) == 0


def test_index__search_for_note_with_None__raises_error() -> None:
    index: Index = Index()

    with pytest.raises(NoteIndexerError):
        # noinspection PyTypeChecker
        index.search_for_note(None)


def test_index__search_for_note_with_empty_string__raises_error() -> None:
    index: Index = Index()

    with pytest.raises(NoteIndexerError):
        # noinspection PyTypeChecker
        index.search_for_note("")


def test_index__search_for_note_with_file_name_not_exists__returns_None() -> None:
    index: Index = Index()

    assert index.search_for_note("i_really_hope_this_file_doesnt_exist.md") is None


def test_index__search_for_note_with_file_name_exists__returns_the_Note() -> None:
    index: Index = Index()
    note: Note = Note(Path("./notes/note1.md"))
    index.register(note)

    assert index.search_for_note("note1.md") == note


def test_index__when_created__repr_string_indicates_that_its_empty() -> None:
    index: Index = Index()

    assert repr(index) == "Index.empty"


def test_index__when_created_with_elements__repr_string_shows_size() -> None:
    index: Index = Index()
    index.register(Note(Path()))

    assert repr(index) == "Index(size=1)"
