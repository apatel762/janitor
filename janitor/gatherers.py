from .notes import Note


class Gatherer:
    """
    Represents a collection of logic that scans the content of a Note and
    gathers information about it.

    The information should be recorded into the Note (you should assume
    that all the Gatherers will mutate the Note that you give it).
    """

    def apply(self, note: Note) -> bool:
        raise NotImplementedError("Use a ")


class ForwardLinkGatherer(Gatherer):
    def __init__(self):
        pass

    def apply(self, note: Note) -> bool:
        """
        Scan the contents of a Note and store all the Forward Links in the
        given Note.

        :param note: The Note that you want to search.
        :return: True if any Forward Links were found, otherwise False.
        """
        # TODO:
        #  - Convert Note to AST
        #  - Find all forward Links
        #  - Stop when you reach the first H2 called Backlinks
        pass
