from janitor.index import Index


def test_index__when_created__repr_string_contains_class_name():
    index = Index()

    assert "Index[" and "]" in repr(index)
