from typing import Any

from pydantic import BaseModel, ConfigDict


class StalcraftEntity(BaseModel):
    """An API object that provides data in a convenient form.

    This class extends from Pydantic's `BaseModel` and is designed to represent API responses in a
    structured and convenient format. When data is returned from the STALCRAFT: X API, the data is
    automatically wrapped in this class for easy access.

    The class supports Pydantic's data validation and serialization, making it easier to handle API
    responses and convert them into Python objects.
    """

    model_config = ConfigDict(validate_by_alias=True)

    def raw(self) -> dict[str, Any]:
        """Raw representation of the object as it was obtained from the STALCRAFT: X API.

        Returns:
            dict[str, Any]: A dictionary containing the raw data of the object as it was received from the API.
        """
        return self.model_dump(by_alias=True, mode="json", exclude_none=True)
