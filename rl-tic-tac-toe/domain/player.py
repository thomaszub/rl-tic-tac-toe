from abc import ABC, abstractmethod

from .board import Board
from .marker import Marker


class Player(ABC):
    _marker: Marker

    def __init__(self, marker: Marker) -> None:
        super().__init__()
        self._marker = marker

    @abstractmethod
    def take_turn(self, board: Board) -> tuple[int, int]:
        pass

    @abstractmethod
    def board_changed(self, new_board: Board, won_or_lost: int) -> None:
        pass

    def marker(self) -> Marker:
        return self._marker
