from os import DirEntry
from typing import List


class Note:
    def __init__(self, path: DirEntry):
        """
        :param path: A path to the Note file where this Note is stored.
        """
        self.path: DirEntry = path
        self.backlinks: List[Note] = []
        self.forward_links: List[ForwardLink] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.path.name}]"


class ForwardLink:
    """
    A forward link is a link that originates from a Note and takes you to
    another Note.
    """

    def __init__(self, origin: Note, destination: Note):
        """
        :param origin: The note that contains the link.
        :param destination: The note that the link is pointing to.
        """
        self.origin: Note = origin
        self.destination: Note = destination

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.origin}, {self.destination}]"
