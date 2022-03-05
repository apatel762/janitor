from pathlib import Path

from janitor.indexer import Indexer


class CrawlerError(Exception):
    pass


class Crawler:
    def __init__(self, crawl_dir: Path):
        if crawl_dir is None:
            raise CrawlerError("Cannot create a crawler without a crawl_dir")

        self.crawl_dir: Path = crawl_dir
        self.index: Indexer = Indexer()

    def go(self):
        pass

    def dump(self):
        pass

    def __len__(self):
        return 0

    def __getitem__(self, index):
        # if index > len(self):
        #     raise IndexError
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}[size={len(self)}]"
