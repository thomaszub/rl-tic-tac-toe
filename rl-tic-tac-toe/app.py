from domain.marker import Marker
from game import Game
from human_player import HumanPlayer


def main():
    playerX = HumanPlayer("Thomas", Marker.X)
    playerO = HumanPlayer("Peter", Marker.O)
    game = Game((playerX, playerO))
    game.start()


if __name__ == "__main__":
    main()
