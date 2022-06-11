import datetime
import hashlib
import os
import time
from functools import cache
from os import DirEntry
from pathlib import Path
from typing import List

import typer

from .gatherers import Gatherer
from .indexer import Index
from .notes import Note
from .typerutils import warn


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

    @cache
    def get_cache_directory(self) -> Path:
        """
        Creates a directory that will be used as a cache. All unimportant files
        (i.e. files that can be re-created) will be stored in this folder.

        The cache directory will be partitioned using a key that is generated
        using the crawl_dir. This ensures that whenever we crawl a directory,
        the cache will always be stored in the same place.

        :return: The path to the cache directory
        """
        cache_home: str = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
        cache_partition_key: str = hashlib.sha256(
            os.path.abspath(self.crawl_dir).encode()
        ).hexdigest()

        cache_path: Path = Path(f"{cache_home}/janitor/{cache_partition_key}")
        cache_path.mkdir(parents=True, exist_ok=True)
        return cache_path

    def go(self) -> None:
        with os.scandir(self.crawl_dir) as sd:
            for entry in sd:  # type: DirEntry
                if not self.validate_entry(entry):
                    continue

                note: Note = Note(path=Path(entry))

                # ensure that the Index is aware of this Note before we
                # gather information about it
                self.index.register(note)

        for gatherer in self.gatherers:  # type: Gatherer
            t0 = time.time()
            for note in self.index:  # type: Note
                gatherer.apply(self.index, note)
            t1 = time.time()
            typer.echo(f"  {repr(gatherer):<30} took {t1 - t0:<10.5f} seconds")

        for broken_link in self.index.broken_links:
            typer.echo(warn(f"broken link: {broken_link}."))

        for orphan in self.index.orphans:
            typer.echo(warn(f"orphan: {orphan}."))

        # persist the index to the filesystem so that the other commands can
        # read the data
        self.index.scan_time = datetime.datetime.now(tz=datetime.timezone.utc)
        self.index.dump(location=self.get_cache_directory())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.crawl_dir}]"
