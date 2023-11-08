class CatalogNotFoundError(Exception):
    def __init__(self, message: str = "Given directory doesn't exist"):
        self.message = message


class FileNotFound(Exception):
    def __init__(self, message: str = "Given file doesn't exist"):
        self.message = message
