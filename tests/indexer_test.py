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
