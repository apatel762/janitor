import os.path
from os import DirEntry
from os import PathLike
from typing import Optional
from typing import Set
from typing import Union


class NoteSerialisationError(Exception):
    pass


class Note:
    def __init__(self, path: Union[DirEntry, PathLike]) -> None:
        """
        :param path: A path to the Note file where this Note is stored.
        """
        self.path: Union[DirEntry, PathLike] = path
        self.backlinks: Set[NoteLink] = set()
        self.forward_links: Set[NoteLink] = set()
        self.sha256_checksum: Optional[str] = None

    def serialise(self) -> dict:
        """
        Convert the metadata for this Note to JSON.

        :return: A dictionary representing the JSON structure of the Note metadata
        """
        if len(self.sha256_checksum) is None:
            raise NoteSerialisationError(
                f"{self} has no SHA-256 checksum recorded. Was the checksum calculated before serialisation?"
            )
        if self.path is None:
            raise NoteSerialisationError(
                f"{self} has no Path associated with it. Something has gone horribly wrong..."
            )
        return {
            "sha256": self.sha256_checksum,
            "path": os.path.abspath(self.path),
            "links": {
                "back": [bl.serialise() for bl in self.backlinks],
                "forward": [fl.serialise() for fl in self.forward_links],
            },
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Note):
            return hash(self) == hash(other)
        else:
            return NotImplemented

    def __hash__(self) -> int:
        """
        Two Note objects are the same if they have the same path.
        """
        return hash(self.path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.path.name}]"


class NoteLink:
    """
    A link is a connection between Note objects that that originates from one
    Note and takes you to another Note.
    """

    def __init__(self, origin: Note, origin_context: str, destination_file_name: str):
        """
        :param origin: The Note that contains the link.
        :param origin_context: The text in the origin Note that contains the link
        :param destination_file_name: The file name that the link is pointing to.
        """
        self.origin: Note = origin
        self.origin_context: str = origin_context
        self.destination_file_name: str = destination_file_name

    def serialise(self) -> dict:
        """
        Convert this NoteLink to JSON.

        :return: A dictionary representing the JSON structure of this NoteLink
        """
        return {
            "destination": self.destination_file_name,
            "context": self.origin_context,
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NoteLink):
            return hash(self) == hash(other)
        else:
            return NotImplemented

    def __hash__(self) -> int:
        """
        Two NoteLink objects are the same if they come from the same Note,
        were found in the same context (line of text in Note) and are pointing
        to the same destination file.
        """
        return hash((self.origin, self.origin_context, self.destination_file_name))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.origin.path.name} -> {self.destination_file_name}]"
