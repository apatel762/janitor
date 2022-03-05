# TODO: make custom error? not sure if needed


class Indexer:
    def __init__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}[{self.__class__.__hash__(self)}]"
