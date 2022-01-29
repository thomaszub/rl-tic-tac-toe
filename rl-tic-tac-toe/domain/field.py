from enum import Enum


class Field(Enum):
    FREE = 1
    X = 2
    O = 3

    def toInt(self, player: "Field") -> int:
        if self == Field.FREE:
            return 0
        if self == player:
            return 1
        else:
            return -1
