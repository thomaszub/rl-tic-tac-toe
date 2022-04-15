from agent_player import QAgentPlayer
from domain.marker import Marker
from game import Game
from human_player import HumanPlayer


def main():
    playerX = HumanPlayer(Marker.X)
    playerO = HumanPlayer(Marker.O)
    game = Game((playerX, playerO))
    game.start()


if __name__ == "__main__":
    main()
