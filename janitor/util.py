import os
from functools import cache
from pathlib import Path


@cache
def get_cache_directory() -> Path:
    return Path(
        f"{os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))}/janitor/"
    )


@cache
def get_tmp_directory() -> Path:
    return get_cache_directory().joinpath("tmp")
