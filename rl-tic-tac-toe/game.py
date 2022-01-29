from random import randint, randrange

from domain.board import Board
from domain.field import Field
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
            player = Field.X if current_player == self._playerX else Field.O
            action = current_player.take_turn(self._board)
            self._board.set_field(action, player)
            # TODO Determine win condition
            current_player.board_changed(self._board, 0)
            current_player = (
                self._playerX if current_player == self._playerO else self._playerO
            )
