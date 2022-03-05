from pathlib import Path


class Note:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def __repr__(self):
        return f"{self.__class__.__name__}[{self.file_path.name}]"
