from typing import Optional, Tuple

from domain.board import Board
from domain.gameresult import GameResult
from domain.marker import Marker
from domain.player import Player


class HumanPlayer(Player):
    def __init__(self, marker: Marker) -> None:
        super().__init__(marker)

    def take_turn(self, board: Board) -> Tuple[int, int]:
        print(board)
        return self._get_user_input(board)

    def board_changed(
        self, new_board: Board, game_result: Optional[GameResult]
    ) -> None:
        pass

    def _get_user_input(self, board: Board) -> tuple[int, int]:
        position = input(f"{self} choose a field (1-3, e.g. 3 1): ").split(" ")
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

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Player {self.marker()}"
