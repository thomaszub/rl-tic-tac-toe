from random import randint
from typing import Tuple

from domain.board import Board
from domain.gameresult import GameResult
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

    def start(self) -> None:
        game_ended = None
        while game_ended == None:
            action = self._current_player.take_turn(self._board)
            gameresult = self._board.mark_position(
                action, self._current_player.marker()
            )
            self._current_player.board_changed(self._board, gameresult)
            if gameresult != None:
                game_ended = True
                self._next_player().board_changed(self._board, gameresult.opposite())
                if self._print_board:
                    print(self._board)
                    if gameresult == GameResult.Won:
                        print(f"{self._current_player} has won!")
                    else:
                        print("The game is a draw!")
            else:
                self._current_player = self._next_player()

    def _next_player(self) -> Player:
        if self._current_player == self._players[0]:
            return self._players[1]
        else:
            return self._players[0]
