from janitor.indexer import Indexer


def test_indexer__when_created__repr_string_contains_class_name():
    index = Indexer()

    assert "Indexer[" and "]" in repr(index)
