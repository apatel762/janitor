import hashlib
from abc import ABC
from abc import abstractmethod
from functools import cache
from typing import Any
from typing import Optional

import pandoc
import typer
from pandoc.types import Header
from pandoc.types import Link
from pandoc.types import Pandoc

from .indexer import Index
from .notes import Note
from .notes import NoteLink
from .typerutils import warn


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

    @cache
    def parse_abstract_syntax_tree(self, note: Note) -> Pandoc:
        """
        Uses the pandoc library to convert a given Markdown Note into a
        Pandoc-flavoured Markdown Abstract Syntax Tree.

        NOTE: from the result, `tree[0]` will give you the metadata
        and `tree[1]` will give you the subtree with the actual text.

        :param note: A Markdown Note object to parse.
        :return: The Pandoc abstract sytax tree of the object.
        """
        return pandoc.read(file=note.path.path, format="markdown")

    @abstractmethod
    def apply(self, index: Index, note: Note) -> bool:
        """
        This method should be overridden by subclasses to implement the
        'gathering' logic.

        :param index: The Note Index.
        :param note: A Markdown Note object to gather information from.
        """
        raise NotImplementedError("Use a subclass!")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{id(self)}]"


class BacklinkGatherer(Gatherer):
    """
    A gatherer that will detect all backlinks for a Note. It works by scanning
    all the forward links for every Note in the Index and storing the inverse
    backlink information from that.

    NOTE: This gatherer should be used AFTER the ForwardLinkGatherer or else
    it will report everything as a broken link.
    """

    def __init__(self) -> None:
        pass

    def apply(self, index: Index, note: Note) -> bool:
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
                # TODO: should there be a separate broken link checker to pick
                #  these up or should I just handle it here?? separate checker
                #  would be nice to keep things clean but handling it here would
                #  be faster
                typer.echo(warn(f"Possible broken link: {link}."))

            # add the NoteLink as a backlink in the other note
            other_note.backlinks.add(link)

        return True


class ForwardLinkGatherer(Gatherer):
    """
    A gatherer for detecting all forward (outgoing) links in a Markdown Note
    file.
    """

    def __init__(self) -> None:
        pass

    def is_backlinks_header(self, elt: Any) -> bool:
        """
        Determine whether a given Pandoc tree element is the backlinks Header.

        :param elt: The Pandoc tree element.
        :return: True if the element is the backlinks Header, otherwise False.
        """
        if not isinstance(elt, Header):
            return False

        # all backlinks headers are H2, so if we aren't looking at a
        # level 2 header, we can leave
        if elt[0] != 2:
            return False

        header_text: str = pandoc.write(elt[2]).strip()
        return header_text == "Backlinks"

    def is_link_to_another_note(self, elt: Any, n: Note) -> bool:
        """
        Determine whether a given Pandoc tree element is a Link.

        :param elt: The Pandoc tree element.
        :return: True if the element is a Link, otherwise False.
        """
        if not isinstance(elt, Link):
            return False

        # for a Link element, it's the third thing which holds the
        # link target (first thing is the attrs and second is the alt
        # text, if any)
        link_target: str = "".join(elt[2])

        return (
            link_target != n.path.name
            and link_target.endswith(".md")
            and not link_target.startswith(".")
            and "http" not in link_target
        )

    def apply(self, index: Index, note: Note) -> bool:
        """
        Scan the contents of a Note, find all Forward Links and store them
        in the given Note.

        :param index: The Note Index.
        :param note: The Note that you want to search.
        :return: True if any Forward Links were found, otherwise False.
        """
        tree: Pandoc = self.parse_abstract_syntax_tree(note)

        for element, path in pandoc.iter(tree[1], path=True):
            # don't want to include any links that come after the Backlinks
            # header (if any) so if we see that we've got to stop
            if self.is_backlinks_header(element):
                break

            # don't care about anything that isn't a link
            if not self.is_link_to_another_note(element, note):
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


class Sha256ChecksumGatherer(Gatherer):
    """
    A gatherer for calculating the SHA-256 checksum for the contents of a
    given file.
    """

    def __init__(self) -> None:
        pass

    def apply(self, index: Index, note: Note) -> bool:
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
