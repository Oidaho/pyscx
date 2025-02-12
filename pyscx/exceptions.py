class BaseAPIException(Exception):
    """Base exception class for handling API-related errors.

    This is the base exception class from which all exceptions related to API operations should inherit.
    It provides a default error message and allows custom error messages to be passed at instantiation.

    Attributes:
        message (str): The error message to be displayed when the exception is raised.
        default_message (str): The default error message used when no custom message is provided.

    Args:
        message (str | None): A custom error message. If not provided, the default message is used.
    """

    default_message = "Oops! Something went wrong inside the API."

    def __init__(self, message: str | None = None) -> None:
        self.message = message

    def __str__(self):
        return self.message if self.message else self.default_message


class MissingTokenError(BaseAPIException):
    """Exception raised when a required token is missing.

    This exception is raised when the API expects a token but it is not found in the API object.

    Args:
        message (str | None): A custom error message. If None, the default message is used.
        **kwargs: Additional keyword arguments to specify the token type.
    """

    def __init__(self, message: str | None = None, **kwargs) -> None:
        super().__init__(message)
        type = kwargs.get("type")
        if type:
            self.default_message = f"The token of type '{type}' is missing from the API object."
        else:
            self.default_message = "The token is missing from the API object."


class InvalidMethodGroup(BaseAPIException):
    """Exception raised when an invalid method group is requested.

    This exception is raised when the API encounters an invalid or nonexistent method group.

    Args:
        message (str | None): A custom error message. If None, the default message is used.
        **kwargs: Additional keyword arguments to specify the invalid method group.
    """

    def __init__(self, message: str | None = None, **kwargs) -> None:
        super().__init__(message)
        group = kwargs.get("group")
        if group:
            self.default_message = f"Не возможно получить группу методов API с именем '{group}'."
        else:
            self.default_message = "Не возможно получить группу методов API."
