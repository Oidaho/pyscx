class BaseAPIException(Exception):
    default_message = "Oops! Something went wrong inside the API."

    def __init__(self, message: str | None = None) -> None:
        self.message = message

    def __str__(self):
        return self.message if self.message else self.default_message


class MissingTokenError(BaseAPIException):
    def __init__(self, message: str | None = None, **kwargs) -> None:
        super().__init__(message)
        type = kwargs.get("type")
        if type:
            self.default_message = f"The token of type '{type}' is missing from the API object."
        else:
            self.default_message = "The token is missing from the API object."


class InvalidMethodGroup(BaseAPIException):
    def __init__(self, message: str | None = None, **kwargs) -> None:
        super().__init__(message)
        group = kwargs.get("group")
        if group:
            self.default_message = f"Не возможно получить группу методов API с именем '{group}'."
        else:
            self.default_message = "Не возможно получить группу методов API."
