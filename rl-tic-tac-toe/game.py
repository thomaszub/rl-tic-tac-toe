from domain.board import Board
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
        pass  # TODO
