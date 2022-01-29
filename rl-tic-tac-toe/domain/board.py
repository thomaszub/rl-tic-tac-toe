from typing import List, Optional, Tuple

from .marker import Marker


class Board:
    _fields: List[List[Optional[Marker]]]

    def __init__(self):
        self._fields = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def mark_position(self, position: Tuple[int, int], marker: Marker):
        if position[0] < 0 or position[0] > 2 or position[1] < 0 or position[1] > 2:
            raise ValueError(f"Position {position} not on board")
        self._fields[position[0]][position[1]] = marker

    def __str__(self) -> str:
        col_strings = [
            "|".join(map(lambda x: " " if x == None else x.__str__(), col))
            for col in self._fields
        ]
        str = "\n-----\n".join(col_strings)
        return str
