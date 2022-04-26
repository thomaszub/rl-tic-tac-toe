from enum import Enum


class Marker(Enum):
    Cross = 1
    Circle = 2

    def __str__(self) -> str:
        if self == Marker.Cross:
            return "X"
        else:
            return "O"
