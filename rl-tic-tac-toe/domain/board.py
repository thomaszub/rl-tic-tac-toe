from typing import List, Tuple

from .field import Field


class Board:
    _fields: List[List[Field]]

    def __init__(self):
        self._fields = [
            [Field.FREE, Field.FREE, Field.FREE],
            [Field.FREE, Field.FREE, Field.FREE],
            [Field.FREE, Field.FREE, Field.FREE],
        ]

    def set_field(self, position: Tuple[int, int], player: Field):
        if player == Field.FREE:
            raise ValueError(f"Player {player} not allowed")
        if position[0] < 0 or position[0] > 2 or position[1] < 0 or position[1] > 2:
            raise ValueError(f"Position {position} not on board")
        self._fields[position[0]][position[1]] = player
