from typing import Any

import pandoc
from pandoc.types import Header
from pandoc.types import Pandoc

from .notes import Note


class Gatherer:
    """
    Represents a collection of logic that scans the content of a Markdown
    Note and gathers information about it.

    The information should be recorded into the Note (you should assume
    that all the Gatherers will mutate the Note that you give it).
    """

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

    def apply(self, note: Note) -> bool:
        """
        This method should be overridden by subclasses to implement the
        'gathering' logic.

        :param note: A Markdown Note object to gather information from.
        """
        raise NotImplementedError("Use a subclass!")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{hash(self)}]"


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

    def is_link(self, elt: Any) -> bool:
        """
        Determine whether a given Pandoc tree element is a Link

        :param elt: The Pandoc tree element
        :return: True if the element is a Link, otherwise False
        """
        # TODO: implement this
        return False

    def apply(self, note: Note) -> bool:
        """
        Scan the contents of a Note, find all Forward Links and store them
        in the given Note.

        :param note: The Note that you want to search.
        :return: True if any Forward Links were found, otherwise False.
        """
        tree: Pandoc = self.parse_abstract_syntax_tree(note)

        for element in pandoc.iter(tree[1]):
            # don't want to include any links that come after the Backlinks
            # header (if any) so if we see that we've got to stop
            if self.is_backlinks_header(element):
                break

            # don't care about anything that isn't a link
            if not self.is_link(element):
                continue

            # TODO: if it's not an internal link, skip

            # TODO: create ForwardLink and append to Note data
            pass

        return True
