class LibraryBaseException(Exception):
    pass


class ItemNotFoundError(LibraryBaseException):
    pass


class OutOfStockError(LibraryBaseException):
    pass


class DuplicateItemError(LibraryBaseException):
    pass