from os import PathLike
from typing import List
from typing import Optional

from .notes import Note


class NoteIndexerError(Exception):
    """
    Thrown whenever there is an error performing an action within the Index.
    """

    pass


class Index:
    """
    The Index represents a collection of Notes that can be serialised to and
    de-serialised from JSON.
    """

    def __init__(self) -> None:
        self.__notes: List[Note] = []

    def register(self, note: Note) -> None:
        """
        Registers a Note with the index (a fancy way of saying that it adds
        it to the Notes list).

        :param note: A Note to add to the index
        """
        self.__notes.append(note)

    def dump(self, location: PathLike) -> bool:
        """
        Dump the indexed content to disk in the JSON format.

        :return: True if the operation was successful, otherwise False.
        """
        return False

    def search_for_note(self, file_name: str) -> Optional[Note]:
        """
        Search the Index for a Note using a file name.

        :param file_name: The filename of the Note that you are looking for
        :return: The Note if we have indexed it, otherwise None
        """
        for note in self:
            if note.path.name == file_name:
                return note
        else:
            return None

    def __len__(self) -> int:
        return len(self.__notes)

    def __getitem__(self, index: int) -> Note:
        if index > len(self):
            raise IndexError
        return self.__notes[index]

    def __repr__(self) -> str:
        name: str = self.__class__.__name__
        size: int = len(self.__notes)

        return f"{name}.empty" if size == 0 else f"{name}(size={size})"
