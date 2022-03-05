import os
from os import DirEntry
from pathlib import Path
from typing import List

import typer

from .gatherers import Gatherer
from .indexer import Index
from .notes import Note


class CrawlerError(Exception):
    pass


class Crawler:
    def __init__(self, crawl_dir: Path) -> None:
        if crawl_dir is None:
            raise CrawlerError("Cannot create a crawler without a crawl_dir")

        self.crawl_dir: Path = crawl_dir
        self.index: Index = Index()
        self.gatherers: List[Gatherer] = []

    def validate_entry(self, entry: DirEntry) -> bool:
        return entry.is_file() and entry.name.endswith(".md")

    def go(self) -> None:
        with os.scandir(self.crawl_dir) as sd:
            for entry in sd:  # type: DirEntry
                if not self.validate_entry(entry):
                    continue

                note: Note = Note(path=entry)

                # ensure that the Index is aware of this Note before we
                # gather information about it
                self.index.register(note)

        # use a progress bar to provide feedback for the user as this
        # could be quite slow depending on how many notes the user has...
        # (takes about 30 seconds for me, and I have about 400 Notes)
        with typer.progressbar(self.index) as pb:
            for note in pb:  # type: Note
                for gatherer in self.gatherers:  # type: Gatherer
                    gatherer.apply(note)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.crawl_dir}]"
