class HttpException(Exception):
    """Exception raised for errors in http responses. (code is better readable if errors raised for failure responses and 
    return values for successful responses)

    Attributes:
        err_code -- html error code
        message -- explanation of the error
    """

    def __init__(self, message, err_code):
        self.message = message
        self.err_code = err_code
        super().__init__(self.message, self.err_code)

