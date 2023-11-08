from builtins import FileNotFoundError


class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""
