from random import randint
from typing import Optional, Tuple

from domain.board import Board
from domain.gameresult import GameResult
from domain.marker import Marker
from domain.player import Player


class Game:
    _board: Board
    _players: Tuple[Player, Player]
    _current_player: Player
    _print_board: bool

    def __init__(
        self, players: Tuple[Player, Player], print_board: bool = True
    ) -> None:
        self._players = players
        if players[0].marker() == players[1].marker():
            raise ValueError("Players have the same marker")
        self._print_board = print_board
        self.reset()

    def reset(self) -> None:
        self._board = Board()
        self._current_player = self._players[randint(0, 1)]

    def start(self) -> Optional[Marker]:
        game_ended = None
        first_turn = True
        while game_ended is None:
            player = self._current_player
            action = player.take_turn(self._board)
            result = self._board.mark_position(action, player.marker())
            if not first_turn:
                opposite_result = None if result is None else result.opposite()
                self._next_player().board_changed(self._board, opposite_result)
            else:
                first_turn = False
            if result is not None:
                game_ended = True
                player.board_changed(self._board, result)
                if self._print_board:
                    print(self._board)
                    if result == GameResult.Won:
                        print(f"{player} has won!")
                    else:
                        print("The game is a draw!")

                if result == GameResult.Won:
                    return player.marker()
                else:
                    return None
            else:
                self._current_player = self._next_player()

    def _next_player(self) -> Player:
        if self._current_player == self._players[0]:
            return self._players[1]
        else:
            return self._players[0]
