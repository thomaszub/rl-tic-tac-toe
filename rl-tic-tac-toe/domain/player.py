from abc import ABC, abstractmethod

from .board import Board


class Player(ABC):
    @abstractmethod
    def take_turn(self, board: Board) -> tuple[int, int]:
        pass

    @abstractmethod
    def board_changed(self, new_board: Board, won_or_lost: int):
        pass
