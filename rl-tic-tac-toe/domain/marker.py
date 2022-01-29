from enum import Enum


class Marker(Enum):
    X = 1
    O = 2

    def __str__(self) -> str:
        if self == Marker.X:
            return "X"
        else:
            return "O"
