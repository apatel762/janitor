import os
from functools import cache
from pathlib import Path


@cache
def get_cache_directory() -> Path:
    cache_path: Path = Path(
        f"{os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))}/janitor/"
    )

    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


@cache
def get_tmp_directory() -> Path:
    tmp_dir: Path = get_cache_directory().joinpath("tmp")

    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir
