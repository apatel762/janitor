from janitor.indexer import Index


def test_indexer__when_created__repr_string_indicates_that_its_empty():
    index = Index()

    assert repr(index) == "Index.empty"


def test_indexer__when_created_with_elements__repr_string_shows_size():
    index = Index()
    index.notes = [1, 2]

    assert repr(index) == "Index(size=2)"
