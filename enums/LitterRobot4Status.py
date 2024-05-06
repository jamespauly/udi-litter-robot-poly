from __future__ import annotations
from enum import Enum

class LitterRobot4StatusMixIn:
    """Litter box status mixin."""

    _text: str | None
    _index: int | None
    _minimum_cycles_left: int

class LitterRobot4Status(LitterRobot4StatusMixIn, Enum):
    """Representation of a Litter-Robot status."""

    def __new__(
            cls, value: str | None, text: str | None, index: int | None = None, minimum_cycles_left: int = 3
    ) -> LitterRobot4Status:
        """Create and return a new Litter Box Status."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj._text = text
        obj._index = index
        obj._minimum_cycles_left = minimum_cycles_left
        return obj

    BONNET_REMOVED = ("BR", "Bonnet Removed", 0)
    CLEAN_CYCLE_COMPLETE = ("CCC", "Clean Cycle Complete", 1)
    CLEAN_CYCLE = ("CCP", "Clean Cycle In Progress", 2)
    CAT_DETECTED = ("CD", "Cat Detected", 3)
    CAT_SENSOR_FAULT = ("CSF", "Cat Sensor Fault", 4)
    CAT_SENSOR_INTERRUPTED = ("CSI", "Cat Sensor Interrupted", 5)
    CAT_SENSOR_TIMING = ("CST", "Cat Sensor Timing", 6)
    DRAWER_FULL_1 = ("DF1", "Drawer Almost Full - 2 Cycles Left", 7, 2)
    DRAWER_FULL_2 = ("DF2", "Drawer Almost Full - 1 Cycle Left", 8, 1)
    DRAWER_FULL = ("DFS", "Drawer Full", 9, 0)
    DUMP_HOME_POSITION_FAULT = ("DHF", "Dump + Home Position Fault", 10)
    DUMP_POSITION_FAULT = ("DPF", "Dump Position Fault", 11)
    EMPTY_CYCLE = ("EC", "Empty Cycle", 12)
    HOME_POSITION_FAULT = ("HPF", "Home Position Fault", 13)
    OFF = ("OFF", "Off", 14)
    OFFLINE = ("OFFLINE", "Offline", 15)
    OVER_TORQUE_FAULT = ("OTF", "Over Torque Fault", 16)
    PAUSED = ("P", "Clean Cycle Paused", 17)
    PINCH_DETECT = ("PD", "Pinch Detect", 18)
    POWER_DOWN = ("PWRD", "Powering Down", 19)
    POWER_UP = ("PWRU", "Powering Up", 20)
    READY = ("RDY", "Ready", 21)
    STARTUP_CAT_SENSOR_FAULT = ("SCF", "Cat Sensor Fault At Startup", 22)
    STARTUP_DRAWER_FULL = ("SDF", "Drawer Full At Startup", 23, 0)
    STARTUP_PINCH_DETECT = ("SPF", "Pinch Detect At Startup", 24)

    # Handle unknown/future unit statuses
    UNKNOWN = (None, "Unknown", 25)

    @property
    def index(self) -> int:
        """Return the minimum number of cycles left based on a litter box's status."""
        return self._index