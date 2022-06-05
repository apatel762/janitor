from os import PathLike
from pathlib import Path

import pytest

from janitor.crawler import Crawler
from janitor.crawler import CrawlerError


def test_crawler__no_dir_provided__raises_crawler_error() -> None:
    with pytest.raises(CrawlerError):
        # noinspection PyTypeChecker
        Crawler(crawl_dir=None)


def test_crawler__when_created__repr_string_shows_size() -> None:
    crawler: Crawler = Crawler(crawl_dir=Path())

    assert repr(crawler) == "Crawler[.]"


def test_crawler__validate_entry__returns_true_when_markdown_file() -> None:
    crawler: Crawler = Crawler(crawl_dir=Path())
    valid: PathLike = Path('./notes/note1.md')

    # noinspection PyTypeChecker
    assert crawler.validate_entry(valid) is True


def test_crawler__validate_entry__returns_false_when_not_markdown_file() -> None:
    crawler: Crawler = Crawler(crawl_dir=Path())
    invalid: PathLike = Path('./notes/')

    # noinspection PyTypeChecker
    assert crawler.validate_entry(invalid) is False


def test_get_cache_directory() -> None:
    crawler: Crawler = Crawler(crawl_dir=Path())
    directory: Path = crawler.get_cache_directory()

    assert ".cache" and "janitor" in str(directory.resolve())
