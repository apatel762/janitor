from pathlib import Path
from typing import List

from .notes import Note


class Index:
    def __init__(self):
        self.notes: List[Note] = []

    def register(self, note: Note):
        """
        Registers a Note with the index (a fancy way of saying that it adds
        it to the Notes list).

        :param note: A Note to add to the index
        """
        self.notes.append(note)

    def dump(self, location: Path) -> bool:
        """
        Dump the indexed content to disk in the JSON format.

        :return: True if the operation was successful, otherwise False.
        """
        return False

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, index):
        if index > len(self):
            raise IndexError
        return self.notes[index]

    def __repr__(self) -> str:
        name: str = self.__class__.__name__
        size: int = len(self.notes)

        return f"{name}.empty" if size == 0 else f"{name}(size={size})"
