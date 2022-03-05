import os.path
from os import DirEntry
from os import PathLike
from typing import List
from typing import Optional
from typing import Union


class NoteSerialisationError(Exception):
    pass


class Note:
    def __init__(self, path: Union[DirEntry, PathLike]) -> None:
        """
        :param path: A path to the Note file where this Note is stored.
        """
        self.path: Union[DirEntry, PathLike] = path
        self.backlinks: List[Note] = []
        self.forward_links: List[ForwardLink] = []
        self.sha256_checksum: Optional[str] = None

    def to_json(self) -> dict:
        if len(self.sha256_checksum) is None:
            raise NoteSerialisationError(
                f"{self} has no SHA-256 checksum recorded. Was the checksum calculated before serialisation?"
            )
        return {
            "sha256": self.sha256_checksum,
            "path": os.path.abspath(self.path),
            "links": {
                "back": [note.path.name for note in self.backlinks],
                "forward": [fl.destination_file_name for fl in self.forward_links],
            },
        }

    def __repr__(self) -> str:
        has_checksum: str = (
            "yes"
            if self.sha256_checksum is not None and len(self.sha256_checksum) > 0
            else "no"
        )
        return (
            f"{self.__class__.__name__}"
            f"[{self.path.name} "
            f"bl={len(self.backlinks)},"
            f"fl={len(self.forward_links)},"
            f"sha256={has_checksum}]"
        )


class ForwardLink:
    """
    A forward link is a link that originates from a Note and takes you to
    another Note.
    """

    def __init__(self, origin: Note, destination_file_name: str):
        """
        :param origin: The note that contains the link.
        :param destination_file_name: The file name that the link is pointing to.
        """
        self.origin: Note = origin
        self.destination_file_name: str = destination_file_name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}[{self.origin} -> {self.destination_file_name}]"
        )
