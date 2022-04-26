from copy import deepcopy
from dataclasses import Field
from typing import Callable, List, Optional, Tuple

from .gameresult import GameResult
from .marker import Marker


class Board:
    _fields: List[List[Optional[Marker]]]

    def __init__(self):
        self._fields = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def mark_position(
        self, position: Tuple[int, int], marker: Marker
    ) -> Optional[GameResult]:
        self._validate_position(position)
        self._set_field(position, marker)
        return self._get_gameresult(position, marker)

    def is_position_free(self, position: Tuple[int, int]) -> bool:
        if self._get_field(position) is None:
            return True
        else:
            return False

    def get_free_positions(self) -> List[Tuple[int, int]]:
        free_fields = []
        for x, col in enumerate(self._fields):
            for y, field in enumerate(col):
                if field is None:
                    free_fields.append((x + 1, y + 1))
        return free_fields

    def get_fields(self) -> List[List[Optional[Marker]]]:
        return deepcopy(self._fields)

    def copy(self) -> "Board":
        copy = Board()
        copy._fields = deepcopy(self._fields)
        return copy

    def _validate_position(self, pos: Tuple[int, int]) -> None:
        if pos[0] < 1 or pos[0] > 3 or pos[1] < 1 or pos[1] > 3:
            raise ValueError(f"Position {pos} not on board")

    def _get_field(self, position: Tuple[int, int]) -> Optional[Marker]:
        return self._fields[position[0] - 1][position[1] - 1]

    def _set_field(self, position: Tuple[int, int], marker: Marker) -> None:
        self._fields[position[0] - 1][position[1] - 1] = marker

    def _get_gameresult(
        self, position: Tuple[int, int], marker: Marker
    ) -> Optional[GameResult]:
        fields = self._fields
        col = position[1] - 1
        row = position[0] - 1
        check = self._field_checker(marker)
        if check(fields[0][col], fields[1][col], fields[2][col]):
            return GameResult.Won
        if check(fields[row][0], fields[row][1], fields[row][2]):
            return GameResult.Won
        if check(fields[0][0], fields[1][1], fields[2][2]):
            return GameResult.Won
        if check(fields[0][2], fields[1][1], fields[2][0]):
            return GameResult.Won
        num_elems = len([field for col in fields for field in col if field is not None])
        if num_elems >= 9:
            return GameResult.Draw
        return None

    def _field_checker(self, marker: Marker) -> Callable[[List[Field]], bool]:
        def _check(*fields: List[Field]) -> bool:
            for field in fields:
                if field != marker:
                    return False
            return True

        return _check

    def __str__(self) -> str:
        col_strings = [
            "|".join(map(lambda x: " " if x is None else x.__str__(), col))
            for col in self._fields
        ]
        str = "\n-----\n".join(col_strings)
        return str
