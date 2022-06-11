from datetime import datetime
from os import PathLike
from typing import Optional
from typing import Set


class NoteSerialisationError(Exception):
    pass


class Note:
    def __init__(self, path: PathLike) -> None:
        """
        :param path: A path to the Note file where this Note is stored.
        """
        self.path: PathLike = path
        self.title: Optional[str] = None
        self.sha256_checksum: Optional[str] = None
        self.last_modified: Optional[datetime] = None
        self.backlinks: Set[NoteLink] = set()
        self.forward_links: Set[NoteLink] = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{'None' if self.path is None else self.path.name}]"


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

    def __repr__(self) -> str:
        # ensure that we have something to include in the repr string even if the
        # information is not present
        origin: str = (
            "None"
            if self.origin is None or self.origin.path is None
            else self.origin.path.name
        )
        return f"{self.__class__.__name__}[{origin} -> {self.destination_file_name}]"
