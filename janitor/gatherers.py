import datetime
import hashlib
from abc import ABC
from abc import abstractmethod
from typing import Optional

import pandoc
from pandoc.types import Pandoc

from .indexer import Index
from .notes import Note
from .notes import NoteLink
from .pandocutils import is_backlinks_header
from .pandocutils import is_header
from .pandocutils import is_link_to_another_note
from .pandocutils import parse_abstract_syntax_tree


class GathererError(Exception):
    """
    An error that is thrown when something goes wrong during the processing
    logic of the Gatherer classes.
    """

    pass


class Gatherer(ABC):
    """
    Represents a collection of logic that scans the content of a Markdown
    Note and gathers information about it.

    The information should be recorded into the Note (you should assume
    that all the Gatherers will mutate the Note that you give it).
    """

    def apply(self, index: Index, note: Note) -> bool:
        if not self.validate_gathering_order(index):
            raise GathererError("Invalid gathering order on " + self.__class__.__name__)

        self.register_with_index(index)
        return self.do_apply(index, note)

    @abstractmethod
    def do_apply(self, index: Index, note: Note) -> bool:
        """
        This method should be overridden by subclasses to implement the
        'gathering' logic.

        The #apply function should be used by external callers.

        :param index: The Note Index.
        :param note: A Markdown Note object to gather information from.
        """
        raise NotImplementedError("Use a subclass!")

    def validate_gathering_order(self, index: Index) -> bool:
        """
        This method should be overridden by subclasses to implement any
        checks around whether the gatherer is being run in the correct
        order or not.

        By default, we return True as we are assuming that most gatherers
        don't care about the order in which they are used.

        :param index: The Note Index.
        """
        return True

    def register_with_index(self, index):
        index.registered_gatherers.add(self.__class__.__name__)

    def __repr__(self) -> str:
        return "Gatherer"


class BacklinkGatherer(Gatherer):
    """
    A gatherer that will detect all backlinks for a Note. It works by scanning
    all the forward links for every Note in the Index and storing the inverse
    backlink information from that.

    Will also check for broken links.
    """

    def __init__(self) -> None:
        pass

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        Using the Index, register backlinks for any Notes that are mentioned
        by the Note that we are currently processing.

        :param index: The Note Index.
        :param note: The Note that you are currently processing.
        :return: True if the operation was successful, otherwise False
        """
        for link in note.forward_links:
            other_note: Optional[Note] = index.search_for_note(
                file_name=link.destination_file_name
            )
            if other_note is None:
                index.broken_links.append(link)
            else:
                # add the NoteLink as a backlink in the other note
                other_note.backlinks.add(link)

        return True

    def validate_gathering_order(self, index: Index) -> bool:
        """
        This gatherer should be used AFTER the ForwardLinkGatherer or else
        it will report everything as a broken link.
        """
        if ForwardLinkGatherer.__name__ not in index.registered_gatherers:
            return False

        return True

    def __repr__(self) -> str:
        return "Gatherer for Backlinks"


class ForwardLinkGatherer(Gatherer):
    """
    A gatherer for detecting all forward (outgoing) links in a Markdown Note
    file.
    """

    def __init__(self) -> None:
        pass

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        Scan the contents of a Note, find all Forward Links and store them
        in the given Note.

        :param index: The Note Index.
        :param note: The Note that you want to search.
        :return: True if any Forward Links were found, otherwise False.
        """
        tree: Pandoc = parse_abstract_syntax_tree(note)

        for element, path in pandoc.iter(tree[1], path=True):
            # don't want to include any links that come after the Backlinks
            # header (if any) so if we see that we've got to stop
            if is_backlinks_header(element):
                break

            # don't care about anything that isn't a link
            if not is_link_to_another_note(element, note):
                continue

            # we want to also record the context of every link
            # this means that we have to capture the content of the parent
            # element for every link; we traverse up the tree by 'one' to do
            # this (using `path[-1]` and then get contents from `[0]`).
            link_context: str = "".join(pandoc.write(path[-1][0])).replace("\n", " ")

            note.forward_links.add(
                NoteLink(
                    origin=note,
                    origin_context=link_context,
                    destination_file_name="".join(element[2]),
                )
            )

        return len(note.forward_links) > 0

    def __repr__(self) -> str:
        return "Gatherer for Forward Links"


class Sha256ChecksumGatherer(Gatherer):
    """
    A gatherer for calculating the SHA-256 checksum for the contents of a
    given file.
    """

    def __init__(self) -> None:
        pass

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        Calculate the SHA-256 checksum for the contents of the given Note and
        store the Hex digest in the Note object.

        :param index: The Note Index.
        :param note: The Note that you want to calculate a checksum for.
        :return: True if the checksum was calculated successfully, otherwise False.
        """
        with open(note.path, "rb") as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)

            note.sha256_checksum = file_hash.hexdigest()

        return True

    def __repr__(self) -> str:
        return "Gatherer for SHA256 Checksums"


class ModifiedTimeGatherer(Gatherer):
    """
    A gatherer for retrieving the 'last modified' time for a given note.
    """

    def __init__(self) -> None:
        pass

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        :param index: The Note Index.
        :param note: The Note that you want to calculate a checksum for.
        :return: True if the mtime was found, otherwise False.
        """
        file_mtime: float = note.path.stat().st_mtime
        note.last_modified = datetime.datetime.fromtimestamp(
            file_mtime, tz=datetime.timezone.utc
        )

        return True

    def __repr__(self) -> str:
        return "Gatherer for File mtimes"


class NoteTitleGatherer(Gatherer):
    """
    A gatherer for retrieving the title of a given note.
    """

    def __init__(self) -> None:
        pass

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        :param index: The Note Index.
        :param note: The Note that you want to calculate a checksum for.
        :return: True if the note title was found, otherwise False.
        """
        tree: Pandoc = parse_abstract_syntax_tree(note)

        for element in pandoc.iter(tree[1]):
            # don't want to include any links that come after the Backlinks
            # header (if any) so if we see that we've got to stop
            if not is_header(element, level=1):
                continue

            # the header text is the third part of the header element, so
            # we need to use `[2]` to extract it, and we need to tell Pandoc
            # to convert it from it's AST format back to a string.
            note.title = pandoc.write(element[2]).replace("\n", "")

        return True

    def __repr__(self) -> str:
        return "Gatherer for Note Titles"


class OrphanNoteGatherer(Gatherer):
    """
    A gatherer to detect orphaned notes (i.e. those that have no backlinks and
    therefore are not mentioned anywhere).
    """

    def __init__(self) -> None:
        pass

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        :param index: The Note Index.
        :param note: The Note that you are currently processing.
        :return: True if the operation was successful, otherwise False
        """
        if len(note.backlinks) == 0:
            index.orphans.append(note)

        return True

    def validate_gathering_order(self, index: Index) -> bool:
        """
        This gatherer should be used AFTER the ForwardLinkGatherer or else
        it will report everything as a broken link.
        """
        if BacklinkGatherer.__name__ not in index.registered_gatherers:
            return False

        return True

    def __repr__(self) -> str:
        return "Gatherer for Orphan Notes"
