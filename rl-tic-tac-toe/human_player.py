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
        return self._get_user_input(board)

    def board_changed(self, new_board: Board, won_or_lost: int) -> None:
        pass

    def _get_user_input(self, board: Board) -> tuple[int, int]:
        position = input(f"Player {self._name} choose a field (1-3, e.g. 3 1): ").split(
            " "
        )
        if len(position) >= 2:
            posX = position[0]
            posY = position[1]
            if posX.isdigit() and posY.isdigit():
                chosen_pos = int(posX), int(posY)
                if board.is_position_free(chosen_pos):
                    return chosen_pos
                else:
                    print(f"Position {chosen_pos} is not free, try again!")
        print("Wrong input, try again!")
        return self._get_user_input(board)
