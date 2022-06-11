from functools import cache
from typing import Any
from typing import Optional

import pandoc
from pandoc.types import Header
from pandoc.types import Link
from pandoc.types import Pandoc

from .notes import Note


@cache
def parse_abstract_syntax_tree(note: Note) -> Pandoc:
    """
    Uses the pandoc library to convert a given Markdown Note into a
    Pandoc-flavoured Markdown Abstract Syntax Tree.

    NOTE: from the result, `tree[0]` will give you the metadata
    and `tree[1]` will give you the subtree with the actual text.

    :param note: A Markdown Note object to parse.
    :return: The Pandoc abstract syntax tree of the object.
    """
    return pandoc.read(file=note.path, format="markdown")


def is_header(elt: Any, level: Optional[int] = None) -> bool:
    """
    Determine whether the given element is a Header, and if so, check
    that the Header is at the given level.

    :param elt: A Pandoc AST element
    :param level: A header level e.g. 2 would represent an H2 element.
    :return: True if the given element is a Header at the given level
    otherwise False
    """
    return isinstance(elt, Header) and (True if level is None else elt[0] == level)


def is_backlinks_header(elt: Any) -> bool:
    """
    Determine whether a given Pandoc tree element is the backlinks Header.

    :param elt: The Pandoc tree element.
    :return: True if the element is the backlinks Header, otherwise False.
    """
    # all backlinks headers are H2, so if we aren't looking at a
    # level 2 header, we can leave
    if not is_header(elt, level=2):
        return False

    header_text: str = pandoc.write(elt[2]).strip()
    return header_text == "Backlinks"


def is_link_to_another_note(elt: Any, n: Note) -> bool:
    """
    Determine whether a given Pandoc tree element is a Link.

    :param elt: The Pandoc tree element.
    :param n: The Note from which the given element originates from
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
