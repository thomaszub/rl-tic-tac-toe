from random import randint, randrange
from typing import Optional, Tuple

from domain.board import Board
from domain.player import Player


class Game:
    _board: Board
    _players: Tuple[Player, Player]
    _current_player: Player

    def __init__(self, players: Tuple[Player, Player]) -> None:
        self._players = players
        if players[0].marker() == players[1].marker():
            raise ValueError("Players have the same marker")
        self.reset()

    def reset(self) -> None:
        self._board = Board()
        self._current_player = self._players[randint(0, 1)]

    def start(self) -> None:
        player_won = None
        while player_won == None:
            action = self._current_player.take_turn(self._board)
            self._board.mark_position(action, self._current_player.marker())
            # TODO Determine win condition
            self._current_player.board_changed(self._board, 0)
            self._current_player = self._next_player()

    def _next_player(self) -> Player:
        if self._current_player == self._players[0]:
            return self._players[1]
        else:
            return self._players[0]
