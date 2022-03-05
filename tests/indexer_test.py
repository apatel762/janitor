from pathlib import Path

from janitor.indexer import Index
from janitor.notes import Note


def test_indexer__when_created__repr_string_indicates_that_its_empty() -> None:
    index = Index()

    assert repr(index) == "Index.empty"


def test_indexer__when_created_with_elements__repr_string_shows_size() -> None:
    index = Index()
    index.register(Note(Path()))

    assert repr(index) == "Index(size=1)"
