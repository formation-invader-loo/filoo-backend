class HttpException(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, message, err_code):
        self.message = message
        self.err_code = err_code
        super().__init__(self.message, self.err_code)

