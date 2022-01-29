from abc import ABC, abstractmethod

from .board import Board


class Player(ABC):
    @abstractmethod
    def take_turn(board: Board) -> tuple[int, int]:
        pass
