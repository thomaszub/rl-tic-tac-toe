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
        self._validate_position(position)
        self._set_field(position, marker)

    def is_position_free(self, position: Tuple[int, int]) -> bool:
        if self._get_field(position) == None:
            return True
        else:
            return False

    def _validate_position(self, position: Tuple[int, int]) -> None:
        if position[0] < 1 or position[0] > 3 or position[1] < 1 or position[1] > 3:
            raise ValueError(f"Position {position} not on board")

    def _get_field(self, position: Tuple[int, int]) -> Optional[Marker]:
        return self._fields[position[0] - 1][position[1] - 1]

    def _set_field(self, position: Tuple[int, int], marker: Marker) -> None:
        self._fields[position[0] - 1][position[1] - 1] = marker

    def __str__(self) -> str:
        col_strings = [
            "|".join(map(lambda x: " " if x == None else x.__str__(), col))
            for col in self._fields
        ]
        str = "\n-----\n".join(col_strings)
        return str
