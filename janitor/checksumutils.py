import hashlib
from os import PathLike


def sha256_checksum(file: PathLike) -> str:
    with open(file, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)

        return file_hash.hexdigest()
