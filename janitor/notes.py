from dataclasses import dataclass
from datetime import datetime
from os import PathLike
from typing import List
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

        # stored during 'scan', used during 'apply'
        self.needs_refresh = False

    @property
    def markdown_backlinks_block(self) -> str:
        """
        Transform the backlinks metadata (held in this object) into a
        Markdown text block. The text block will always start with an
        H2 header, followed by a list of backlinks with context.
        """
        if len(self.backlinks) == 0:
            return ""

        elements: List[str] = ["## Backlinks", ""]

        for backlink in sorted(self.backlinks):
            elements.append(f"- {backlink.origin_as_markdown()}")
            elements.append(f"  - {backlink.origin_context}")

        return "\n".join(elements)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{'None' if self.path is None else self.path.name}]"


@dataclass(frozen=True, order=True)
class NoteLink:
    """
    A link is a connection between Note objects that that originates from one
    Note and takes you to another Note.
    """

    # The path to the Note from which this link originates
    origin_note_path: PathLike
    # The title of the Note from which this link originates
    origin_note_title: str
    # The text in the origin Note that contains the link
    origin_context: str
    # The file name that the link is pointing to.
    destination_file_name: str

    def origin_as_markdown(self) -> str:
        return f"[{self.origin_note_title}]({self.origin_note_path.name})"
