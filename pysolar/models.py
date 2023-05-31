"""Models."""

from pydantic import BaseModel, validator


class SolarPanelPaybackRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Solar panel payback request model."""

    consumption: float
    cost: float
    wp: float

    @validator("consumption", "cost", "wp")
    def set_consumption(cls, val: float) -> None:
        """Check whether value is non negative or is not too big."""
        if val < 0:
            raise ValueError("value is less than 0")
        if val > 10000000:
            raise ValueError("value is too big. Maximum allowed value is 10000000.")
