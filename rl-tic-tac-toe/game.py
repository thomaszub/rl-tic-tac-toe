from random import randint, randrange
from typing import Optional

from domain.board import Board
from domain.marker import Marker
from domain.player import Player


class Game:
    _board: Board
    _playerX: Player
    _playerO: Player

    def __init__(self, playerX: Player, playerO: Player):
        self._board = Board()
        self._playerX = playerX
        self._playerO = playerO

    def reset(self):
        self._board = Board()

    def start(self):
        starting_player = randint(0, 1)
        if starting_player == 0:
            current_player = self._playerX
        else:
            current_player = self._playerO
        player_won = None
        while player_won == None:
            player_marker = Marker.X if current_player == self._playerX else Marker.O
            action = current_player.take_turn(self._board)
            self._board.mark_position(action, player_marker)
            # TODO Determine win condition
            current_player.board_changed(self._board, 0)
            current_player = (
                self._playerX if current_player == self._playerO else self._playerO
            )
