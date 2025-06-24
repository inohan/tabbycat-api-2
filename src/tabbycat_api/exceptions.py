class ParseException(Exception):
    """Exception raised for errors in the parsing process."""
    pass

class HTTPStatusException(Exception):
    """Exception raised for HTTP-related errors."""
    status: int