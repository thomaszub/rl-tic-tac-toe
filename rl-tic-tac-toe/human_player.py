from typing import overload

from domain.board import Board
from domain.player import Player


class HumanPlayer(Player):
    _name: str

    def __init__(self, name: str):
        self._name = name

    def take_turn(self, board: Board) -> tuple[int, int]:
        print(board)
        return self._get_user_input()

    def board_changed(self, new_board: Board, won_or_lost: int):
        pass

    def _get_user_input(self) -> tuple[int, int]:
        position = input(f"Player {self._name} choose a field (1-3, e.g. 3 1): ").split(
            " "
        )
        if len(position) >= 2:
            posX = position[0]
            posY = position[1]
            if posX.isdigit() and posY.isdigit():
                return int(posX), int(posY)
        print("Wrong input, try again!")
        return self._get_user_input()
