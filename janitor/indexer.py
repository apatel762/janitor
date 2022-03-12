import json
import os
from os import PathLike
from pathlib import Path
from typing import List
from typing import Optional

import typer

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
        if type(note) is not Note:
            raise NoteIndexerError(
                f"Cannot register a {repr(type(note))}-type object with the Index."
            )

        self.__notes.append(note)

    def dump(self, location: PathLike) -> bool:
        """
        Dump the indexed content to disk in the JSON format.

        :return: True if the operation was successful, otherwise False.
        """
        if location is None:
            raise NoteIndexerError(
                "Cannot dump the Index to disk without providing a location first."
            )

        target_location: PathLike = Path(os.path.join(location, "index.json"))
        typer.echo(f"Dumping {self} to: {target_location}")

        # serialise all the notes and construct the JSON index
        index_as_json: dict = self.serialise()

        with open(target_location, "w", encoding="utf-8") as f:
            json.dump(index_as_json, f, ensure_ascii=False, indent=4)

        return True

    def serialise(self) -> dict:
        """
        Transforms the Index and its contents into a JSON structure

        :return: A dictionary object representing the JSON structure of the Index.
        """
        index_as_json: dict = {
            os.path.basename(note.path): note.serialise() for note in self.__notes
        }

        return index_as_json

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
