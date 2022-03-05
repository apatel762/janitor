from pathlib import Path

import pytest

from janitor.crawler import Crawler
from janitor.crawler import CrawlerError


def test_crawler__no_dir_provided__raises_crawler_error():
    with pytest.raises(CrawlerError):
        # noinspection PyTypeChecker
        Crawler(crawl_dir=None)


def test_crawler__when_created__repr_string_shows_size():
    crawler: Crawler = Crawler(crawl_dir=Path())

    assert repr(crawler) == "Crawler[.]"
