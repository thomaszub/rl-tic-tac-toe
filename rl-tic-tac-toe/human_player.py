from domain.board import Board
from domain.marker import Marker
from domain.player import Player


class HumanPlayer(Player):
    _name: str

    def __init__(self, name: str, marker: Marker) -> None:
        super().__init__(marker)
        self._name = name

    def take_turn(self, board: Board) -> tuple[int, int]:
        print(board)
        return self._get_user_input()

    def board_changed(self, new_board: Board, won_or_lost: int) -> None:
        pass

    def _get_user_input(self) -> tuple[int, int]:
        position = input(f"Player {self._name} choose a field (1-3, e.g. 3 1): ").split(
            " "
        )
        if len(position) >= 2:
            posX = position[0]
            posY = position[1]
            if posX.isdigit() and posY.isdigit():
                return int(posX) - 1, int(posY) - 1
        print("Wrong input, try again!")
        return self._get_user_input()
