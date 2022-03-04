from pathlib import Path


class CrawlerError(Exception):
    pass


class Crawler:
    def __init__(self, crawl_dir: Path):
        if crawl_dir is None:
            raise CrawlerError("Cannot create a crawler without a crawl_dir")

        self.crawl_dir = crawl_dir

    def dump_results_to_disk(self):
        pass

    def __len__(self):
        return 0

    def __getitem__(self, index):
        # if index > len(self):
        #     raise IndexError
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}[size={len(self)}]"


class Note:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def __repr__(self):
        return f"{self.__class__.__name__}[{self.file_path.name}]"
