from abc import ABC, abstractmethod
from typing import Optional, Tuple

from .board import Board
from .gameresult import GameResult
from .marker import Marker


class Player(ABC):
    _marker: Marker

    def __init__(self, marker: Marker) -> None:
        super().__init__()
        self._marker = marker

    @abstractmethod
    def take_turn(self, board: Board) -> Tuple[int, int]:
        pass

    @abstractmethod
    def board_changed(
        self, new_board: Board, game_result: Optional[GameResult]
    ) -> None:
        pass

    def marker(self) -> Marker:
        return self._marker

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.marker()}"
