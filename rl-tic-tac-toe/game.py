from random import randint, randrange
from typing import Optional, Tuple

from domain.board import Board
from domain.marker import Marker
from domain.player import Player


class Game:
    _board: Board
    _players: Tuple[Player, Player]

    def __init__(self, players: Tuple[Player, Player]) -> None:
        self._board = Board()
        self._players = players
        if players[0].marker() == players[1].marker():
            raise ValueError("Players have the same marker")

    def reset(self) -> None:
        self._board = Board()

    def start(self) -> None:
        current_player_num = randint(0, 1)
        current_player = self._players[current_player_num]
        player_won = None
        while player_won == None:
            action = current_player.take_turn(self._board)
            self._board.mark_position(action, current_player.marker())
            # TODO Determine win condition
            current_player.board_changed(self._board, 0)

            current_player_num = (current_player_num + 1) % 2
            current_player = self._players[current_player_num]
