import datetime
from abc import ABC
from abc import abstractmethod
from typing import Optional

import pandoc
from pandoc.types import Pandoc

from .checksumutils import sha256_checksum
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

    def apply(self, index: Index, note: Note) -> None:
        if not self.validate_gathering_order(index):
            raise GathererError("Invalid gathering order on " + self.__class__.__name__)

        self.register_with_index(index)

        self.pre_apply(index, note)
        self.do_apply(index, note)
        self.post_apply(index, note)

    def pre_apply(self, index: Index, note: Note) -> None:
        pass

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

    def post_apply(self, index: Index, note: Note) -> None:
        pass

    def validate_gathering_order(self, index: Index) -> bool:
        """
        This method should be overridden by subclasses to implement any
        checks around whether the gatherer is being run in the correct
        order or not.

        By default, we check if the file mtime gatherer has run because
        that one is the most important.

        :param index: The Note Index.
        """
        return ModifiedTimeGatherer.__name__ in index.registered_gatherers

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
                index.broken_links.add(link)
            else:
                # add the NoteLink as a backlink in the other note
                other_note.backlinks.add(link)

        return True

    def validate_gathering_order(self, index: Index) -> bool:
        """
        This gatherer should be used AFTER the ForwardLinkGatherer or else
        it will report everything as a broken link.

        We also must ensure that the NoteTitleGatherer has run, because we
        need to have note titles in order to create links.
        """
        return (
            NoteTitleGatherer.__name__ in index.registered_gatherers
            and ForwardLinkGatherer.__name__ in index.registered_gatherers
        )

    def __repr__(self) -> str:
        return "Gatherer for Backlinks"


class ForwardLinkGatherer(Gatherer):
    """
    A gatherer for detecting all forward (outgoing) links in a Markdown Note
    file.
    """

    def __init__(self) -> None:
        pass

    def pre_apply(self, index: Index, note: Note) -> None:
        """
        Clear out the forward links so that we can re-generate them
        reliably now without worrying about possible duplicates (where
        the link origin and destination is the same but the context is
        different).
        """
        note.forward_links = set()

    def do_apply(self, index: Index, note: Note) -> bool:
        """
        Scan the contents of a Note, find all Forward Links and store them
        in the given Note.

        :param index: The Note Index.
        :param note: The Note that you want to search.
        :return: True if any Forward Links were found, otherwise False.
        """
        tree: Pandoc = parse_abstract_syntax_tree(note.path)

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
                    origin_note_path=note.path,
                    origin_note_title=note.title,
                    origin_context=link_context,
                    destination_file_name="".join(element[2]),
                )
            )

        return len(note.forward_links) > 0

    def post_apply(self, index: Index, note: Note) -> None:
        """
        Clear out backlinks so that we can reliably reproduce them from
        scratch later on without duplicates
        """
        note.backlinks = set()

        # clear the backlinks of the notes that this one is pointing to
        # AND mark those notes for refresh by bumping their last_modified
        # value
        for fl in note.forward_links:
            n = index.search_for_note(file_name=fl.destination_file_name)
            if n is None:
                continue

            n.backlinks = {bl for bl in n.backlinks if bl.origin_note_path != note.path}
            n.last_modified = datetime.datetime.now(tz=datetime.timezone.utc)

    def validate_gathering_order(self, index: Index) -> bool:
        """
        We must ensure that the NoteTitleGatherer has run, because we need
        to have note titles in order to create links.
        """
        return NoteTitleGatherer.__name__ in index.registered_gatherers

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
        note.sha256_checksum = sha256_checksum(note.path)

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

    def validate_gathering_order(self, index: Index) -> bool:
        """
        Ensure that this one is the first gatherer to run
        :param index: The Note Index.
        """
        return len(index.registered_gatherers) == 0 or (
            len(index.registered_gatherers) == 1
            and ModifiedTimeGatherer.__name__ in index.registered_gatherers
        )

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
        tree: Pandoc = parse_abstract_syntax_tree(note.path)

        for element in pandoc.iter(tree[1]):
            # don't want to include any links that come after the Backlinks
            # header (if any) so if we see that we've got to stop
            if not is_header(element, level=1):
                continue

            # the header text is the third part of the header element, so
            # we need to use `[2]` to extract it, and we need to tell Pandoc
            # to convert it from it's AST format back to a string.
            note.title = pandoc.write(element[2]).replace("\n", "")
            break

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
            index.orphans.add(note)

        return True

    def validate_gathering_order(self, index: Index) -> bool:
        """
        This gatherer should be used AFTER the BacklinkGatherer or else
        it won't be able to see which notes are orphans
        """
        return BacklinkGatherer.__name__ in index.registered_gatherers

    def __repr__(self) -> str:
        return "Gatherer for Orphan Notes"
