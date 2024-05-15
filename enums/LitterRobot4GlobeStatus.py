from __future__ import annotations
from enum import Enum

class LitterRobot4GlobeStatusMixIn:
    """Globe status mixin."""

    _text: str | None
    _index: int | None

class LitterRobot4GlobeStatus(LitterRobot4GlobeStatusMixIn, Enum):
    """Representation of a Litter-Robot Globe status."""

    def __new__(
            cls, value: str | None, text: str | None, index: int
    ) -> LitterRobot4GlobeStatus:
        """Create and return a new Litter Box Globe Status."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj._text = text
        obj._index = index
        return obj

    OFF = ("OFF", "Off", 0)
    ON = ("ON", "On", 1)
    AUTO = ("AUTO", "Auto", 2)

    @property
    def index(self) -> int:
        """Return the index of the Litter-Robot Globe status."""
        return self._index