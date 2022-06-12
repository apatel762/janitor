import datetime
import os
import pickle
from os import PathLike
from pathlib import Path
from typing import List
from typing import Optional
from typing import Set

import typer

from .notes import Note
from .notes import NoteLink


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
        # the time when the index was last used
        self.use_time: Optional[datetime.datetime] = None
        self.registered_gatherers: Set[str] = set()
        self.broken_links: Set[NoteLink] = set()
        self.orphans: Set[Note] = set()

    def register(self, note: Note) -> None:
        """
        Registers a Note with the index (a fancy way of saying that it adds
        it to the Notes list).

        :param note: A Note to add to the index
        """
        if type(note) is not Note:
            raise NoteIndexerError(
                f"Cannot register a {repr(type(note))}-type object with the Index."
            )

        self.__notes.append(note)

    @staticmethod
    def load(folder_containing_the_index: PathLike):
        file: Path = Path(os.path.join(folder_containing_the_index, "index.pickle"))
        with open(file, "rb") as f:
            return pickle.load(f)  # type: Index

    def dump(self, location: PathLike) -> bool:
        """
        Dump the indexed content to disk in the JSON format.

        :param location: The folder that you want to put the dumped index in
        :return: True if the operation was successful, otherwise False.
        """
        if location is None:
            raise NoteIndexerError(
                "Cannot dump the Index to disk without providing a location first."
            )

        target_location: PathLike = Path(os.path.join(location, "index.pickle"))
        typer.echo(f"Dumping {self} to: {target_location}")

        # record the current time into the index so that we can use it
        # later on to avoid looking at notes that haven't been modified
        # since the scan
        self.use_time = datetime.datetime.now(tz=datetime.timezone.utc)

        with open(target_location, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

        return True

    def search_for_note(self, file_name: str) -> Optional[Note]:
        """
        Search the Index for a Note using a file name.

        :param file_name: The filename of the Note that you are looking for
        :return: The Note if we have indexed it, otherwise None
        """
        if file_name is None or len(file_name) == 0:
            raise NoteIndexerError(
                f"Cannot search for Note in Index with name: {file_name}"
            )

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
