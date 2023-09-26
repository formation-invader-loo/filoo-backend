class CollectionAlreadyExists(Exception):
    """Exception raised for errors that are Caused if a Collection already exists.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CollectionDoesNotExist(Exception):
    """Exception raised for errors that are Caused if a Collection does not exist.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DocumentAlreadyExists(Exception):
    """Exception raised for errors that are Caused if a Document already exists.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DocumentDoesNotExist(Exception):
    """Exception raised for errors that are Caused if a Document does not exist.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
