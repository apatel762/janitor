from os import DirEntry
from os import PathLike
from typing import List
from typing import Union


class Note:
    def __init__(self, path: Union[DirEntry, PathLike]) -> None:
        """
        :param path: A path to the Note file where this Note is stored.
        """
        self.path: Union[DirEntry, PathLike] = path
        self.backlinks: List[Note] = []
        self.forward_links: List[ForwardLink] = []
        self.sha256_checksum: str = ""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"[{self.path.name} "
            f"bl={len(self.backlinks)},"
            f"fl={len(self.forward_links)},"
            f"sha256={'yes' if len(self.sha256_checksum) > 0 else 'no'}]"
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
